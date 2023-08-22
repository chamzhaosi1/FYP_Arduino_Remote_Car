import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RomoComponent } from './romo.component';

describe('RomoComponent', () => {
  let component: RomoComponent;
  let fixture: ComponentFixture<RomoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RomoComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RomoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
