import { Component, OnInit, ElementRef} from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { RomoService } from '../services/romo.service'
import { LiveStreamingService } from '../services/live-streaming.service';
import { MqttWebsocketService } from '../services/mqtt.service';
import { IMqttMessage } from "ngx-mqtt";

@Component({
  selector: 'app-romo',
  templateUrl: './romo.component.html',
  styleUrls: ['./romo.component.css']
})
export class RomoComponent implements OnInit {

  mac_address : string = ""
  username: string = ""
  localVideo: any;
  remoteVideo: any; 
  
  constructor (private route: ActivatedRoute, 
    private romoService:RomoService,
    private elementRef: ElementRef,
    private livestreaming: LiveStreamingService,
    private readonly eventMqtt: MqttWebsocketService){}

  ngOnInit(): void {
    this.route.paramMap.subscribe(param => {
      this.mac_address = param.get('mac_address')!.toString()
    })

    this.getUserName()
    this.sendDeviceReadyMQTT()
  }

  getUserName(){
    this.romoService.getRomoUser('romo_user_detail', this.mac_address).subscribe({
      next : (response:any) => {
        console.log(response)
        this.username = response.body["username"]

        this.localVideo = this.elementRef.nativeElement.querySelector('#localVideo')
        this.remoteVideo = this.elementRef.nativeElement.querySelector('#remoteVideo')
        this.livestreaming.connectWebSocket(this.username, this.mac_address,this.localVideo, this.remoteVideo, "romo")
      }
    })
  }

  sendDeviceReadyMQTT(){
    let pubtopic = "device_connect_status"

    setInterval(()=> {
      // Get current date and time (timestamp)
      let timestamp: number = Date.now();
      
      const message = {
        "datetime": timestamp, 
        "mac_address": this.mac_address
      }
      this.eventMqtt.publish(pubtopic, JSON.stringify(message)).subscribe()

    }, 5000)

  }
}
