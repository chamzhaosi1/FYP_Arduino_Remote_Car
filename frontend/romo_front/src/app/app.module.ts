import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http'
import { CookieService } from 'ngx-cookie-service';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { DashboardComponent } from './dashboard/dashboard.component';
import { RegisterComponent } from './register/register.component';
import { HeaderComponent } from './header/header.component';
import { LogoutComponent } from './logout/logout.component';
import { AuthorizedComponent } from './authorized/authorized.component';

import { IMqttServiceOptions, MqttModule } from "ngx-mqtt";
import { environment as env } from '../environments/environment.prod';
import { ControlComponent } from './control/control.component';
import { RomoComponent } from './romo/romo.component';
import { SnapshotComponent } from './snapshot/snapshot.component';
import { IntruderComponent } from './intruder/intruder.component';
import { ManualComponent } from './manual/manual.component';

const MQTT_SERVICE_OPTIONS: IMqttServiceOptions = {
  hostname: env.mqtt.server,
  port: env.mqtt.port,
  protocol: (env.mqtt.protocol === "wss") ? "wss" : "ws",
  username: env.mqtt.username,
  password: env.mqtt.password,
  path: env.mqtt.path,
};

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    DashboardComponent,
    RegisterComponent,
    HeaderComponent,
    LogoutComponent,
    AuthorizedComponent,
    ControlComponent,
    RomoComponent,
    SnapshotComponent,
    IntruderComponent,
    ManualComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule,
    ReactiveFormsModule,
    HttpClientModule,
    MqttModule.forRoot(MQTT_SERVICE_OPTIONS),
  ],
  providers: [CookieService],
  bootstrap: [AppComponent]
})
export class AppModule { }
