import {Component, Inject, OnInit} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MAT_DIALOG_DATA, MatDialogModule, MatDialogRef} from '@angular/material/dialog';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {StockDataService} from '../service/stock-data.service';
import {MatSnackBar} from '@angular/material/snack-bar';

@Component({
  selector: 'app-add-stock-dialog',
  templateUrl: './add-stock-dialog.component.html',
  styleUrls: ['./add-stock-dialog.component.css']
})
export class AddStockDialogComponent implements OnInit {

  form: FormGroup = new FormGroup({
    symbol: new FormControl({value: this.data['1. symbol'], disabled: true}, Validators.required),
    purchaseDate: new FormControl('', Validators.required),
    amount: new FormControl('', Validators.required),
    purchasePrice: new FormControl('', Validators.required),
  });
  error: string | null;
  msg: string | null;

  constructor(@Inject(MAT_DIALOG_DATA) public data: { defaultValue: any }, public dialogRef: MatDialogRef<AddStockDialogComponent>,
              private stockDataService: StockDataService, private snackBar: MatSnackBar) {
  }

  ngOnInit(): void {
  }

  // tslint:disable-next-line:typedef
  submit() {
    if (this.form.valid) {
      console.log(this.form.value);
      this.form.value.symbol = this.data['1. symbol'];
      this.stockDataService.addStockToPortFolio(this.form.value).subscribe(
        data => {
          this.dialogRef.close();
          console.log(data);
          this.snackBar.open('Successfully added to your portfolio', 'Dismiss');
        },
        err => {
          this.dialogRef.close();
          console.log(err);
          this.snackBar.open('Failed to add stock to your portfolio', 'Dismiss');
        }
      );
    }
  }


}
