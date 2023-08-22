import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { UsersService } from '../services/users.service';
import { AuthorizedService } from '../services/authorized.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-authorized',
  templateUrl: './authorized.component.html',
  styleUrls: ['./authorized.component.css']
})
export class AuthorizedComponent implements OnInit {

  /* FormData is specifically designed for sending form data, 
  including files, in an HTTP request. It provides a convenient and 
  efficient way to send files, especially large files, 
  from the client-side to the server-side.

  When you use an interface with key-value pairs,
  Angular will serialize the data as JSON, which cannot include file data. 
  The FormData object, on the other hand, 
  can handle file data and also allows you to append additional fields, 
  such as text input values, to the request body.

  When you send data as FormData, 
  the browser will automatically set the Content-Type header to multipart/form-data,  
  which is the appropriate content type for sending files over HTTP. */
  new_img_info?= new FormData();
  noImgToShow: any;
  generalMessage?: string;
  imgURLArray: any[] = [];
  name: string = ""
  authImgUploadForm: any;
  authImgCaptureForm: any;
  personID : number[] = [];
  uniquePersonNameArray : string[] = []
  personImageInfoArray : any[] = []

  constructor(private loginService: UsersService, 
    private router: Router, 
    private authImgService: AuthorizedService) {
    this.authImgUploadForm = new FormGroup({
      upload_image: new FormControl('', [Validators.required]),
      person_name: new FormControl('', [Validators.required])
    })

    this.authImgCaptureForm = new FormGroup({
      person_name: new FormControl('', [Validators.required]),
    })
  }

  get Upload_image() {
    return this.authImgUploadForm.get("upload_image")
  }

  get Person_name() {
    return this.authImgUploadForm.get("person_name")
  }

  get Capture_person_name(){
    return this.authImgCaptureForm.get("person_name")
  }

  ngOnInit(): void {
    this.loginService.getAutheToken('user').subscribe({
      next: (response: any) => {
        // console.log(response)
        let first_name: string = response.body['user_info']['first_name'];
        let last_name: string = response.body['user_info']['last_name'];
        this.name = (first_name + " " + last_name);
        this.getAuthImg()
      },
      error: (error) => {
        this.router.navigate(['/login'])
      }
    })
  }

  uploadImgChange($event: any) {
    // when the file uploader is changed, the formdata of the key authorized_img will also be changed
    this.new_img_info?.append("authorized_img", $event.target.files[0])
    // console.log($event.target.files[0])
  }

  authImgUploadFormSubmit() {
    this.new_img_info?.append('person_name', this.Person_name.value.replace(/ /g, "_"));
    // console.log(this.new_img_info)
    this.authImgService.uploadAuthImg('upl_auth_img', this.new_img_info!).subscribe({
      next: (response) => {
        // Because the image is storage in the backend server,
        // so if i do the array append is useless
        this.getAuthImg()
        this.clearForm()
      },
      error: (error) => {
        // if with an error message with code 401 or 404, this means "Not token found or Unauthenticated"
        if (error.status !== 400 && error.error !== null) {
          this.router.navigate(['/login'])
        }
      }
    })
  }

  clearForm() {
    let imgNameInpField = this.Person_name
    imgNameInpField.reset("")

    let upImgFileField = this.Upload_image
    upImgFileField.reset("")
  }

  getAuthImg() {
    this.authImgService.getAuthImg('get_auth_img').subscribe({
      next: (response: any) => {
        // console.log(response)
        if (response['image_info'].length >= 1) {
          // if using the upload function, then we need clear the array before append
          this.uniquePersonNameArray = []
          this.personImageInfoArray = []

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
          this.uniquePersonNameArray = [...new Set(personName)];

          // to record the first 
          let prevValue = this.uniquePersonNameArray[0]
          // to record the id and image info
          let imageInfo = {}
          // to group the same name 
          let subarrayImageInfo : any[] = []
          
          for(let i = 0; i<this.imgURLArray.length; i++){
            imageInfo = {'image': this.imgURLArray[i]['image'], 'id': this.imgURLArray[i]['id']}
            // if the person is same, then append to the array
            if(this.imgURLArray[i]['name'] === prevValue){
              subarrayImageInfo.push(imageInfo)
            }else{
              // once the name is differen then append the above array to the parent array
              this.personImageInfoArray.push(subarrayImageInfo);
              // set the new first array element
              subarrayImageInfo = [imageInfo]
              // update the previous element name
              prevValue = this.imgURLArray[i]['name'] 
            }
          }

          // append the last group of array into the parent array 
          this.personImageInfoArray.push(subarrayImageInfo);

        } else {
          // Because i change the coding structure.
          // If do not has any data in the database, an empty array will also be returned.
          // This means "DoesNotExist" error will be raise in the database
          // Remark: different with the dashboard romo list
          this.noImgToShow = true
          this.generalMessage = "Please upload your first authorized image!"
        }
      },
      error: (error) => {
        console.log(error)
        // If not found the romo device, http status code will be 404
        // but without any error message 
        if (error.status === 404 && error.error === null) {
          this.generalMessage = "Please upload your first authorized image!"
          this.noImgToShow = true;
        } else {
          // if with an error message, this means "Not token found"
          this.router.navigate(['/login'])
        }
      }
    })
  }

  // id for database image id
  // index for image array element index
  deleteImage(id: number, parentIndex: number, childIndex:number) {
    this.authImgService.deleteAuthImg('del_auth_img', id).subscribe({
      next: (response) => {
        if (response.status === 204) {
          // remove the element by index
          if( this.personImageInfoArray[parentIndex].length > 1){
              this.personImageInfoArray[parentIndex]?.splice(childIndex, 1)
            }else{
              // if only one element then remove the empty array from this.personImageInfoArray
              this.personImageInfoArray?.splice(parentIndex, 1)
              this.uniquePersonNameArray?.splice(parentIndex, 1)
            }
        }

        // if all of the image had been delete,
        // then showing the message to user
        if (this.uniquePersonNameArray!.length <= 0) {
          this.noImgToShow = true
          this.generalMessage = "Please upload your first authorized image!"
        }
      },
      error: (error) => {
        console.log(error)
        // If not found the romo device, http status code will be 404
        // but without any error message 
        if (error.status === 404 && error.error === null) {
          console.log("Something error happend, authorized image cannot be deleted!")
        } else {
          // if with an error message, this means "Not token found"
          this.router.navigate(['/login'])
        }
      }
    })
  }

  camera() {
    let person_name = this.Capture_person_name.value
    // console.log(person_name)
    this.router.navigate(["/snapshot", person_name])
  }
}
