import { Component, OnInit, ElementRef} from '@angular/core';
import { UsersService } from '../services/users.service';
import { AuthorizedService } from '../services/authorized.service';
import { Router } from '@angular/router';
import { FaceRecognizationService } from '../services/face-recognization.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-snapshot',
  templateUrl: './snapshot.component.html',
  styleUrls: ['./snapshot.component.css']
})
export class SnapshotComponent implements OnInit {
  new_img_info?= new FormData();
  name: string = ""
  localVideo: any; 
  person_name: string = "";
  isPressSnapshotBtn : Boolean = false;
  errorMessage: string = "";
  isShowErrorMessage: Boolean = false;
  deviceOwnerName?: string = ""
  deviceMacAddress?: string = ""
  isLoadingShow : Boolean = false;

  constructor(private loginService: UsersService, 
    private router: Router, 
    private route: ActivatedRoute, 
    private faceRecognizationService: FaceRecognizationService,
    private elementRef: ElementRef,
    private authImgService: AuthorizedService,
    ){
  }

  ngOnInit(): void {
    this.loginService.getAutheToken('user').subscribe({
      next: (response: any) => {
        console.log(response)
        let first_name: string = response.body['user_info']['first_name'];
        let last_name: string = response.body['user_info']['last_name'];
        this.name = (first_name + " " + last_name);
        this.deviceOwnerName = response.body['user_info']['username'];
        this.localVideo = this.elementRef.nativeElement.querySelector('#localVideo');

        this.route.paramMap.subscribe(param => {
          this.person_name = param.get('person_name')!.toString().replace(/ /g, "_")
        })
        
        this.connectFaceDetection()
      },
      error: (error) => {
        this.router.navigate(['/login'])
      }
    })
  }

  blobToFile(blob: Blob, fileName: string): File {
    const fileOptions: FilePropertyBag = { type: blob.type };
    return new File([blob], fileName, fileOptions);
  }

  connectFaceDetection(){
    this.isLoadingShow = true;
    this.faceRecognizationService.start(this.localVideo, "", "face_detection", this.deviceOwnerName!, "");
  }

  onLoadedFaceVideoMetadata(event:any){
    this.isLoadingShow = false;
  }

  sendImageToBackend(data: any): void {
    const blob = new Blob([data], { type: 'image/jpeg' });
    const image_file = this.blobToFile(blob, "camera.jpg")
    console.log(image_file)

    this.new_img_info?.append("authorized_img", image_file)
    this.new_img_info?.append("person_name", this.person_name)
    this.authImgService.uploadAuthImg("upl_auth_img", this.new_img_info).subscribe({
      next : (response:any) => {
        this.isPressSnapshotBtn = !this.isPressSnapshotBtn
      }
    })
  }

  retrieveCap(){
    let timeout = 1.5
    console.log("Wait Capture image ready....")

    setTimeout(() => {
      this.faceRecognizationService.retrieveCap({"userName": this.deviceOwnerName}).subscribe({
        next: (response:any) => {
          console.log(response)
          if (response.type == 'text/plain'){
            this.errorMessage = "Please make sure your face inside the box!"
            this.isShowErrorMessage = !this.isShowErrorMessage
            this.isPressSnapshotBtn = !this.isPressSnapshotBtn
          }else{
            this.sendImageToBackend(response);
          }
        }
      })
    }, timeout * 1000);
  }

  snapshot(){
    this.isPressSnapshotBtn = !this.isPressSnapshotBtn
    this.faceRecognizationService.snapshot({"label": this.person_name}).subscribe({
      next: (response:any) => {
        console.log(response)
        if (response === "successfully"){
          this.retrieveCap()
        }
      }
    }
  )}


  finish(){
    // close the livestreaming
    this.faceRecognizationService.stop()
    this.router.navigate(['/authorized'])
  }
}
