import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UsersService } from '../services/users.service';
import { ROMO } from '../interfaces/romo';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { checkMacAdd } from '../validators/checkMacAdd.validators';
import { RomoService } from '../services/romo.service'
import { Subscription } from 'rxjs';
import { MqttWebsocketService } from '../services/mqtt.service';
import { IMqttMessage } from "ngx-mqtt";

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  name: string = ""
  joytstickImgUrl: string = "../../assets/joystick.jpg"
  keyboardImgUrl: string = "../../assets/keyboard_mouse.jpg"
  checkIconUrl: string = "../../assets/check-mark.png"
  romoRegisterForm: any;
  controlSelectionForm: any;
  notRomoDeviceFound: boolean = true;
  romo_detail?: ROMO[] = [];
  new_romo_info?: ROMO;
  showErrorMessage: Boolean = false;
  errorMessage?: string
  dev_active_timestamp: number[] = [];
  dev_status: string = "Not Ready - Offline"
  check_dev_active_interval: any[] = [];
  timestampNum: number = -1;

  deviceOwnerName?: string
  deviceMacAddress?: string

  isDeviceReady: boolean[] = [false] // <- need chg
  subscription!: Subscription;

  constructor(private loginService: UsersService, private router: Router, private romoService: RomoService, private readonly eventMqtt: MqttWebsocketService) {
    this.romoRegisterForm = new FormGroup({
      device_mac_address: new FormControl('', [Validators.required, checkMacAdd.checkMacAddValidations]),
      label_name: new FormControl('', [Validators.required])
    })

    this.controlSelectionForm = new FormGroup({
      devicesSelection: new FormControl('keyboard_mouse', [Validators.required]),
    })
  }

  get Mac_address() {
    return this.romoRegisterForm.get('device_mac_address')
  }

  get Label_name() {
    return this.romoRegisterForm.get('label_name')
  }

  get Devices_selection() {
    return this.controlSelectionForm.get('devicesSelection')
  }

  ngOnInit(): void {
    // get observable object
    this.loginService.getAutheToken('user').subscribe({
      next: (response: any) => {
        console.log(response)
        let first_name: string = response.body['user_info']['first_name'];
        let last_name: string = response.body['user_info']['last_name'];
        this.name = (first_name + " " + last_name);
        this.deviceOwnerName = response.body['user_info']['username'];

        this.getRomoDetail();
      },
      error: (error) => {
        this.router.navigate(['/login'])
      }
    })

    this.devStatusSubTop(); // <- need chg
  }

  connectROMO(mac_address: any) {
    // once connect to the live streaming, then unsubscribe the mqtt
    this.subscription.unsubscribe()

    let dev_mac_address = mac_address.innerHTML
    let control_selected = this.Devices_selection.value
    this.router.navigate(['/control', dev_mac_address, control_selected])
  }

  deleteROMO(mac_address: any, index: number) {
    mac_address = mac_address.innerHTML
    console.log(index)
    console.log(mac_address)
    this.romoService.deleteRomo('romo_delete', mac_address).subscribe({
      next: (response: any) => {
        // if successfully delete the object in backend
        if (response.status === 204) {
          // then remove the object element from the array
          this.romo_detail?.splice(index, 1)

          if (this.romo_detail!.length <= 0) {
            this.notRomoDeviceFound = true
          }
        }
      },
      error: (error) => {
        console.log(error)
        // If not found the romo device, http status code will be 404
        // but without any error message 
        if (error.status === 404 && error.error === null) {
          console.log("Something error happend, ROMO device cannot be deleted!")
        } else {
          // if with an error message, this means "Not token found"
          this.router.navigate(['/login'])
        }
      }
    })
  }

  submitRegisterForm() {
    this.new_romo_info = {
      romo_label: this.Label_name.value,
      mac_address: this.Mac_address.value,
      status: "New Registration"
    }

    console.log(this.new_romo_info)
    this.romoService.romoRegister('romo_register', this.new_romo_info).subscribe({
      next: (response: any) => {
        console.log(response)
        // append the new romo detail to the array
        this.romo_detail?.push(response.body);
        this.adjustTimeFormat();
        this.notRomoDeviceFound = false
        this.showErrorMessage = false;

        // clear the form value
        this.resetForm()
      },
      error: (error) => {
        // if the mac address has been exsits
        // backend will return 400 bad request
        this.showErrorMessage = true;
        this.errorMessage = error.error["message"];
      }
    })
  }

  getRomoDetail() {
    this.romoService.getRomoDetail('romo_detail').subscribe({
      next: (response: any) => {
        console.log(response);
        // if the romo device is only one,
        // backend will be returned one object in json format
        if (response.body['romo_info'].length >= 1) {
          this.romo_detail = response.body['romo_info'];
        } else {
          // if the romo device are multiple
          // backend will be returned an object json array
          this.romo_detail?.push(response.body['romo_info']);
        }
        // console.log(this.romo_detail)

        // this.initLastestStatus(); // <- need change
        this.adjustTimeFormat();
        this.notRomoDeviceFound = false;
      },
      error: (error) => {
        console.log(error)
        // If not found the romo device, http status code will be 404
        // but without any error message 
        if (error.status === 404 && error.error === null) {
          this.notRomoDeviceFound = true;
        } else {
          // if with an error message, this means "Not token found"
          this.router.navigate(['/login'])
        }
      }
    })
  }

  // if the last status in backend is ready then connect button will be able to press
  initLastestStatus() {
    for (let i = 0; i < this.romo_detail!.length; i++) {
      this.isDeviceReady[i] = this.romo_detail![i]["status"] === "Ready - Online" ? true : false
    }
  }

  adjustTimeFormat() {
    this.romo_detail?.forEach(element => {
      // console.log(element['last_active'])

      if (element['last_active']!.includes('T')) {
        // replace the string T "2023-05-25T21:53:14" to space
        element['last_active'] = element['last_active']?.replace('T', ' ')
      }

      // if the string has "," which mean it already convert to format that we want, not need do again
      if (!element['last_active']!.includes(',')) {
        // convert to reable data time format
        element['last_active'] = this.dateTimeConvert(element['last_active'])
      }

    });
  }

  // Clear the form input
  resetForm() {
    let labNameInpField = this.Label_name
    labNameInpField.reset("")

    let macAddInpField = this.Mac_address
    macAddInpField.reset("")
  }

  devStatusSubTop() {
    let subtopic = "device_connect_status"
    this.subscription = this.eventMqtt.subscribe(subtopic)
      .subscribe((data: IMqttMessage) => {

        let item = JSON.parse(data.payload.toString());

        // convert the timestamp to date (string to number)
        this.timestampNum = parseInt(item["datetime"], 10);

        // update romo info in the array
        for (let i = 0; i < this.romo_detail!.length; i++) {
          // if the mac address is the same
          // console.log(dev_mac_address)
          if (this.romo_detail![i]["mac_address"] === item["mac_address"]) {
            this.romo_detail![i]["last_active"] = this.dateTimeConvert(this.timestampNum)

            // every second check the dev active status
            console.log(this.timestampNum)
            this.checkRomoDevLastActive(i)

            // update the romo last active status to backend
            this.updateRomoDevLastActive(i)
          }
        }
      });
  }

  updateRomoDevLastActive(indexROMO: number) {
    // the last_active need to use timestamp format to backend
    let new_romo_detial: ROMO = {
      romo_label: this.romo_detail![indexROMO]["romo_label"],
      mac_address: this.romo_detail![indexROMO]["mac_address"],
      status: this.romo_detail![indexROMO]["status"],
      last_active: String(Math.floor(this.timestampNum / 1000))
    }

    // console.log(new_romo_detial['last_active'])

    this.romoService.romoUpdate('romo_update', new_romo_detial).subscribe({})
  }

  // check romo device last active status
  checkRomoDevLastActive(indexROMO: number) {
    if (this.check_dev_active_interval[indexROMO] === undefined) {
      this.check_dev_active_interval[indexROMO] = setInterval(() => {
        let current_timestamp = new Date().getTime();
        this.dev_active_timestamp[indexROMO] = this.timestampNum;

        if (current_timestamp - this.dev_active_timestamp[indexROMO] < 30000) {
          this.isDeviceReady[indexROMO] = true;
          this.romo_detail![indexROMO]["status"] = "Ready - Online";
        } else {
          this.isDeviceReady[indexROMO] = false;
          this.romo_detail![indexROMO]["status"] = "Not Ready - Offline";
          clearInterval(this.check_dev_active_interval[indexROMO]);
          this.check_dev_active_interval[indexROMO] = undefined;

          // update the romo last active status to backend
          // for after connect to the live streaming
          this.updateRomoDevLastActive(indexROMO)
        }

        console.log(indexROMO + " " + current_timestamp + " -> " + this.romo_detail![indexROMO]["status"])
      }, 3000)
    }
  }

  dateTimeConvert(timestampNum: any) {
    let dev_last_avtive: Date | string;
    // console.log(timestampNum)

    // convert the timestamp to date (plain text)
    dev_last_avtive = new Date(timestampNum)

    // convert to simple datatime format
    dev_last_avtive = dev_last_avtive.toLocaleString('en-MY', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: 'numeric',
      minute: 'numeric',
      second: 'numeric',
      hour12: true
    });

    return dev_last_avtive
  }
}
