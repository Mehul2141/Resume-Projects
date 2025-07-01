import {Component, OnInit} from '@angular/core';
import {TokenStorageService} from '../service/token-storage.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-toolbar',
  templateUrl: './toolbar.component.html',
  styleUrls: ['./toolbar.component.css']
})
export class ToolbarComponent implements OnInit {

  isLoggedIn = false;

  constructor(private tokenStorageService: TokenStorageService, private router: Router) {
  }

  ngOnInit(): void {
    this.tokenStorageService.isLoggedIn.subscribe((c) => {
      this.isLoggedIn = c;
    });
    console.log(this.isLoggedIn);
  }

  logout() {
    this.tokenStorageService.signOut();
    this.isLoggedIn = false;
    this.router.navigate(['/login']);
  }

}
