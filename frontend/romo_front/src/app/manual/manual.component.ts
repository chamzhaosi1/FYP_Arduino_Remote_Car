import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UsersService } from '../services/users.service';

@Component({
  selector: 'app-manual',
  templateUrl: './manual.component.html',
  styleUrls: ['./manual.component.css']
})
export class ManualComponent {
  constructor(private loginService: UsersService, private router: Router){}

  name: string = "";
  keyboard_label:string = "../../assets/keyboard_label.png";
  joystick_label:string = "../../assets/joystick_label.png";

  ngOnInit(): void {
    // get observable object
    this.loginService.getAutheToken('user').subscribe({
      next: (response: any) => {
        console.log(response)
        let first_name: string = response.body['user_info']['first_name'];
        let last_name: string = response.body['user_info']['last_name'];
        this.name = (first_name + " " + last_name);
      },
      error: (error) => {
        this.router.navigate(['/login'])
      }
    })
  }
}
