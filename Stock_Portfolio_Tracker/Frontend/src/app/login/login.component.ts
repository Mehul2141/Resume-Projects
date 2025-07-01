import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {FormControl, FormGroup} from '@angular/forms';
import {AuthService} from '../service/auth.service';
import {TokenStorageService} from '../service/token-storage.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  form: FormGroup = new FormGroup({
    username: new FormControl(''),
    password: new FormControl(''),
  });
  error: string | null;


  submit() {
    if (this.form.valid) {
      this.error = null;
      this.authService.login(this.form.value).subscribe(
        data => {
          console.log(data);
          this.tokenStorage.saveToken(data.token);
          this.tokenStorage.saveUser(data.email);
          this.router.navigate(['/home']);
        },
        err => {
          console.log(err);
          this.error = 'Login Failed';
        }
      );
    }
  }

  constructor(private authService: AuthService, private tokenStorage: TokenStorageService, private router: Router) { }

  ngOnInit(): void {
    this.error = null;
  }

}
