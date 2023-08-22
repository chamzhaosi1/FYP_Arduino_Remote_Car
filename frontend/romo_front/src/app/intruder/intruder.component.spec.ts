import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IntruderComponent } from './intruder.component';

describe('IntruderComponent', () => {
  let component: IntruderComponent;
  let fixture: ComponentFixture<IntruderComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ IntruderComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(IntruderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
