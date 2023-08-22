import { Component, OnInit } from '@angular/core';
import { UsersService } from '../services/users.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-logout',
  templateUrl: './logout.component.html',
  styleUrls: ['./logout.component.css']
})
export class LogoutComponent implements OnInit {
  constructor(
    private loginService: UsersService,
    private router: Router) { }

  ngOnInit(): void {
    this.loginService.postLogout('logout').subscribe({
      next: (response) => {
        this.router.navigate([''])
      }
    })
  }
}
