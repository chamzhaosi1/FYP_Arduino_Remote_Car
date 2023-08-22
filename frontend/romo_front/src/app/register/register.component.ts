import { Component } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { User } from '../interfaces/user'
import { UsersService } from '../services/users.service'; 
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  registerForm: any;
  showGeneralError: boolean = false;
  generalError: string = '';
  showNoSameError: boolean = false;
  noSameError: string = 'Both are not same, Please try again!'

  constructor(private userService: UsersService, private router: Router) {
    this.registerForm = new FormGroup({
      username: new FormControl('', [Validators.required]),
      first_name: new FormControl('', [Validators.required]),
      last_name: new FormControl('', [Validators.required]),
      email: new FormControl('', [Validators.required, Validators.email]),
      password: new FormControl('', [Validators.required, Validators.minLength(8)]),
      confirm_password: new FormControl('', [Validators.required, Validators.minLength(8)]),
    })
  }

  get Username() {
    return this.registerForm.get('username')
  }

  get Password() {
    return this.registerForm.get('password')
  }

  get First_name() {
    return this.registerForm.get('first_name')
  }

  get Last_name() {
    return this.registerForm.get('last_name')
  }

  get Email() {
    return this.registerForm.get('email')
  }

  get Confirm_password() {
    return this.registerForm.get('confirm_password')
  }

  // to check whether the confirm_password's length fullfil the minimum
  // and then whether typo the password previously.
  onKeyupEntry(input: any) {
    if (input.value.length >= 8) {
      if (this.Password.value !== input.value) {
        this.showNoSameError = true;
      } else {
        this.showNoSameError = false;
      }
    }
  }

  submitRegister() {
    let newUser: User = {
      username: this.Username.value,
      password: this.Password.value,
      first_name: this.First_name.value,
      last_name: this.Last_name.value,
      email: this.Email.value
    }

    this.userService.postRegister('register', newUser).subscribe({
      next: (response) => {
        this.router.navigate([''])
      },
      error: (error) => {
        // to clear the previous message, if error second time
        this.generalError = ''

        if (error.error['username']) {
          this.generalError += "Username already exists"
        }

        if (error.error['email']) {
          if (this.generalError !== '') {
            this.generalError += " and "
          }
          this.generalError += "Email already exists"
        }

        this.showGeneralError = true
      }
    })
  }

}
