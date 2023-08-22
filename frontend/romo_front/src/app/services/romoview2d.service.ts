import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class Romoview2dService {

  constructor() { }

  redraw(m: any){
    // Mecanum
    m.clearRect(0, 0, 200,200);
    m.strokeStyle = 'black';
    m.lineWidth = 1;
    
    // Left-Front
    m.beginPath();    m.rect(33, 25, 33, 50);     m.stroke();
    m.moveTo(33, 33.5); m.lineTo(66, 66.5);       m.stroke();
    this.draw_cartesian_pos(m, -(33+(33/2)), (25+(50/2)), 'purple', 6)

    // Right-Front
    m.beginPath();    m.rect(134, 25, 33, 50);     m.stroke();
    m.moveTo(134, 66.5); m.lineTo(167, 33.5);       m.stroke();
    this.draw_cartesian_pos(m, (33+(33/2)), (25+(50/2)), 'purple', 6)
    
    // Left-Back
    m.beginPath();    m.rect(33, 125, 33, 50);     m.stroke();
    m.moveTo(33, 166.5); m.lineTo(66, 133.5);       m.stroke();
    this.draw_cartesian_pos(m, -(33+(33/2)), -(25+(50/2)), 'purple', 6)
    
    // Right-Back
    m.beginPath();    m.rect(134, 125, 33, 50);     m.stroke();
    m.moveTo(134, 133.5); m.lineTo(167,166.5);       m.stroke();
    this.draw_cartesian_pos(m, (33+(33/2)), -(25+(50/2)), 'purple', 6)

    // Mecanum Body
    m.beginPath();    m.rect(67, 37.5, 66, 125);     m.stroke();
  }

  // draw the line which represent the mecanum wheel putting method (diamond or x shape)
  draw_cartesian_pos(context:any, x:number, y:number, color:string, size:number) {
    if (color == null) {
        color = '#000';
    }
    if (size == null) {
        size = 5;
    }
    context.beginPath();
    context.lineWidth = 1;
    context.fillStyle = color;
    context.fillRect(x+100-(size/2), -(y-100)-(size/2), size, size);
    context.fill();
    context.closePath();
  }

  // draw the line which represent the mecanum wheel moving direction and rpm
  mecanum_dir(context:any, offset_x:number ,offset_y:number,ang:number, power:number){
    context.beginPath();
    context.lineWidth = 4;
    let radial2 = power*60/300;
    var xx=Math.sin(ang*Math.PI/180)*Math.abs(radial2);
    var yy=Math.cos(ang*Math.PI/180)*Math.abs(radial2);
    if(radial2>=0){
        context.strokeStyle = 'green';
        context.moveTo(offset_x, offset_y); context.lineTo(offset_x+xx,offset_y-yy); context.stroke();
    }else{
        context.strokeStyle = 'red';
        context.moveTo(offset_x, offset_y); context.lineTo(offset_x-xx,offset_y+yy); context.stroke();
    }
    context.closePath();
  }

}
