import { Component, NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { RegisterComponent } from './register/register.component';
import { LogoutComponent } from './logout/logout.component';
import { AuthorizedComponent } from './authorized/authorized.component';
import { ControlComponent } from './control/control.component';
import { RomoComponent } from './romo/romo.component';
import { SnapshotComponent } from './snapshot/snapshot.component';
import { IntruderComponent } from './intruder/intruder.component';
import { ManualComponent } from './manual/manual.component';

const routes: Routes = [
  { path: '', component: DashboardComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'logout', component: LogoutComponent },
  { path: 'manual', component: ManualComponent },
  { path: 'authorized', component: AuthorizedComponent },
  { path: 'intruder', component: IntruderComponent },
  { path: 'snapshot/:person_name', component: SnapshotComponent },
  { path: 'control/:mac_address/:control_type', component: ControlComponent },
  { path: 'login_romo/:mac_address', component: RomoComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
