import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UsersService } from '../services/users.service';
import { IntrusionService } from '../services/intrusion.service';
import { FormBuilder, FormGroup, FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-intruder',
  templateUrl: './intruder.component.html',
  styleUrls: ['./intruder.component.css']
})
export class IntruderComponent implements OnInit{
  deviceOwnerName: string = ""
  name: string = ""
  imageDataArray: any[] = []
  new_img_info?= new FormData();
  uniqueIntrNameArray : string[] = []
  intrImageInfoArray : any[] = []
  intrInfoArray : any[] = []
  noImgToShow: any;
  generalMessage?: string;
  imgURLArray: any[] = [];
  intrConvertAuthForm: any;

  constructor(
    private loginService: UsersService, 
    private router: Router, 
    private intrusionService : IntrusionService,
    private formBuilder: FormBuilder
  ){}

  // get Person_name(){
  //   return this.intrConvertAuthForm.get("person_name")
  // }

  ngOnInit(): void {
    this.loginService.getAutheToken('user').subscribe({
      next: (response: any) => {
        console.log(response)
        let first_name: string = response.body['user_info']['first_name'];
        let last_name: string = response.body['user_info']['last_name'];
        this.name = (first_name + " " + last_name);
        this.deviceOwnerName = response.body['user_info']['username'];
        this.getIntrImg()
      },
      error: (error) => {
        this.router.navigate(['/login'])
      }
    })
  }

  createIntrConvertAuthForm(){
    this.intrConvertAuthForm =  this.formBuilder.group({})
    this.uniqueIntrNameArray.forEach((item, index) => {
      this.intrConvertAuthForm?.addControl(`intruder-${index}`, this.formBuilder.control('', Validators.required));
    })
  }


  getIntrImg(){
    this.intrusionService.getIntrImg('get_intr_img').subscribe({
      next: (response: any) => {
        if (response['image_info'].length >= 1) {
          // if using the upload function, then we need clear the array before append
          this.uniqueIntrNameArray = []
          this.intrImageInfoArray = []

          this.noImgToShow = false;
          this.imgURLArray = response['image_info'];

          // sort the object based on the name, 
          // becuase if later upload a image which may same name as the first element
          this.imgURLArray.sort((a, b) => {
            const nameA = a.name.toLowerCase();
            const nameB = b.name.toLowerCase();
          
            if (nameA < nameB) {
              return -1;
            } else if (nameA > nameB) {
              return 1;
            } else {
              return 0;
            }
          });

          // get all the person name 
          let personName : string[] = [];
          this.imgURLArray.forEach((element) =>{
            personName.push(element['name'])
            
          })

          // remove the duplicate person name
          this.uniqueIntrNameArray = [...new Set(personName)];

          // to record the first 
          let prevValue = this.uniqueIntrNameArray[0]
          // to record the id and image info
          let imageInfo = {}
          // to record the intr info
          let intrInfo = {}
          // to group the same name 
          let subarrayImageInfo : any[] = []
          // to group the same name's intrusion info
          let subarrayIntrInfo : any[] = []
          
          for(let i = 0; i<this.imgURLArray.length; i++){
            imageInfo = {'image': this.imgURLArray[i]['image']}
            intrInfo = {'mac_address': this.imgURLArray[i]['mac_address'], 
                        'date_time': this.imgURLArray[i]['date_time'].replace('T', ' ').split(".")[0],
                        'id': this.imgURLArray[i]['id']}
            // if the person is same, then append to the array
            if(this.imgURLArray[i]['name'] === prevValue){
              subarrayImageInfo.push(imageInfo)
              subarrayIntrInfo.push(intrInfo)
            }else{
              // once the name is differen then append the above array to the parent array
              this.intrImageInfoArray.push(subarrayImageInfo);
              this.intrInfoArray.push(subarrayIntrInfo);
              // set the new first array element
              subarrayImageInfo = [imageInfo]
              subarrayIntrInfo = [intrInfo]
              // update the previous element name
              prevValue = this.imgURLArray[i]['name'] 
            }
          }

          // append the last group of array into the parent array 
          this.intrImageInfoArray.push(subarrayImageInfo);
          this.intrInfoArray.push(subarrayIntrInfo);
          this.createIntrConvertAuthForm()

        } else {
          // Because i change the coding structure.
          // If do not has any data in the database, an empty array will also be returned.
          // This means "DoesNotExist" error will be raise in the database
          // Remark: different with the dashboard romo list
          this.noImgToShow = true
          this.generalMessage = "No intrusion has occurred before!"
        }
      },
      error: (error) => {
        console.log(error)
        // If not found the romo device, http status code will be 404
        // but without any error message 
        if (error.status === 404 && error.error === null) {
          this.generalMessage = "No intrusion has occurred before!"
          this.noImgToShow = true;
        } else {
          // if with an error message, this means "Not token found"
          this.router.navigate(['/login'])
        }
      }
    })
  }  

  // getLatestIntrInfo(){
  //   let lastestDatatimeElement;

  //   for(let j = 0; j< this.intrInfoArray.length; j++){
  //     if (this.intrInfoArray[j].length > 1){
  //       let latestDatetime = this.intrInfoArray[j][0]['date_time']; // Assume the first datetime is the latest initially
  //       lastestDatatimeElement = [this.intrInfoArray[j][0]]

  //       for (let i = 1; i < this.intrInfoArray[j].length; i++) {
  //         const currentDatetime = this.intrInfoArray[j][i]['date_time'];
  //         if (currentDatetime > latestDatetime) {
  //           latestDatetime = currentDatetime;
  //           lastestDatatimeElement = [this.intrInfoArray[j][i]]
  //         }
  //       }

  //       this.intrInfoArray[j] = lastestDatatimeElement
  //     }
  //   }
  // }

  // Form for convert intruder to authorized
  intrConvertAuthFormSubmit(event:any){
    let html_element_id = event.target[0].id
    let array_index = html_element_id.split("-")[1]
    let intruder_img_label = this.uniqueIntrNameArray[array_index]
    let person_name = this.intrConvertAuthForm.get(html_element_id).value
    let intruder_db_id = this.intrInfoArray[array_index][0]['id']

    let conver_img_info = {
      "intruder_img_label" : intruder_img_label,
      "person_name" : person_name,
      "intruder_db_id" : intruder_db_id
    }
    this.intrusionService.updateIntrImg('cvt_intr_auth_img', conver_img_info).subscribe({
      next : (response:any) => {
        console.log(response)
        if (response.ok){
          this.deleteImage(intruder_db_id, array_index)
        }
      }
    })
  }

  // id for database image id
  // index for image array element index
  deleteImage(id: number, index: number) {
    this.intrusionService.deleteIntrImg('del_intr_img', id).subscribe({
      next: (response) => {
        if (response.status === 204) {
          // remove the element by index
          this.intrInfoArray?.splice(index, 1)
          this.intrImageInfoArray?.splice(index, 1)
          this.uniqueIntrNameArray?.splice(index, 1)
        }

        // if all of the image had been delete,
        // then showing the message to user
        if (this.uniqueIntrNameArray!.length <= 0) {
          this.noImgToShow = true
          this.generalMessage = "No intrusion has occurred before!"
        }
        
      },
      error: (error) => {
        console.log(error)
        // If not found the romo device, http status code will be 404
        // but without any error message 
        if (error.status === 404 && error.error === null) {
          console.log("Something error happend, intruder's image cannot be deleted!")
        } else {
          // if with an error message, this means "Not token found"
          this.router.navigate(['/login'])
        }
      }
    })
  }
}
