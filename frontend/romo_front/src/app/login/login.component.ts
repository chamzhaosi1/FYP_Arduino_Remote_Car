import { Component, OnInit, Type } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { UsersService } from '../services/users.service';
import { User } from '../interfaces/user'
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  imgLogoPath: string = "../../assets/romo_logo.png";
  loginForm: any;
  notFoundError: boolean = false;
  errorMessage: string = "null";

  constructor(private loginService: UsersService, private router: Router) {
    this.loginForm = new FormGroup({
      username: new FormControl('', [Validators.required]),
      password: new FormControl('', [Validators.required])
    })
  }

  ngOnInit(): void {
    this.loginService.getAutheToken('user').subscribe({
      next: (response) => {
        this.router.navigate([''])
      },
    })
  }

  get Username() {
    return this.loginForm.get('username')
  }

  get Password() {
    return this.loginForm.get('password')
  }

  submitLogin() {
    let user: User = {
      username: this.Username.value,
      password: this.Password.value
    }

    this.loginService.postLogin('login', user).subscribe({
      next: (response) => {
        // get the response status code
        let status: number = response.status;

        // if equals 200, then redirest to the dashboard page
        if (status == 200) {
          this.router.navigate([''])
          this.notFoundError = false
        }
      },
      error: (error) => {
        this.errorMessage = "Invalid username or password, Please try again!"
        this.notFoundError = true
      }
    })
  }
}
