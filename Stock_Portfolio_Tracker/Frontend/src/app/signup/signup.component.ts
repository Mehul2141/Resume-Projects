import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {FormControl, FormGroup} from '@angular/forms';
import {AuthService} from '../service/auth.service';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {

  form: FormGroup = new FormGroup({
    email: new FormControl(''),
    name: new FormControl(''),
    password: new FormControl(''),
  });
  error: string | null;
  msg: string | null;

  submit() {
    if (this.form.valid) {
      this.error = null;
      this.msg = null;
      this.authService.register(this.form.value).subscribe(
        data => {
          console.log(data);
          this.msg = 'Registration successful';
        },
        err => {
          console.log(err);
          this.error = 'Registration failed';
        }
      );
    }
  }

  constructor(private authService: AuthService) {
  }

  ngOnInit(): void {
  }

}
