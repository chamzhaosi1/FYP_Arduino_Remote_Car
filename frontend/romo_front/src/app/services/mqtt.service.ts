import { Injectable } from '@angular/core';
import { IMqttMessage, MqttService } from "ngx-mqtt";
import { Observable } from "rxjs";

@Injectable({
  providedIn: 'root'
})

export class MqttWebsocketService {
  private endpoint: string;

  constructor(private _mqttService: MqttService) {
    this.endpoint = 'romo';
  }

  subscribe(subtopic: string): Observable<IMqttMessage> {
    let topicName = `${this.endpoint}/${subtopic}`;   
    return this._mqttService.observe(topicName);
  }

  publish(subtopic: string, message: string): Observable<void> {
    let topicName = `${this.endpoint}/${subtopic}`;
    return this._mqttService.publish(topicName, message)
  }
}

