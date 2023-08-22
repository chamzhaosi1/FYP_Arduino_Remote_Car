import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent {
  constructor() { }

  smallLogoUrl: string = "../../assets/romo_logo_sm.png";
  personimage: string = "../../assets/man.png";
  @Input() userFullName: string = ""

  getFullName($event: string) {
    this.userFullName = $event
  }
}
