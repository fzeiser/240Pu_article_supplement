//////////////////////////////////////////////////////
//	Script to plot f.g. matrices of 89,90Y          //
//	Cecilie, Dec 2014                               //
//      ////////////////////////////////////            //
//  changes to plot m_alfna, Fabio, Feb 2015
//////////////////////////////////////////////////////
{

	// starting root stuff
	gROOT->SetStyle("Plain");
	gStyle->SetOptTitle(1);
	gStyle->SetOptStat(0);
	gStyle->SetFillColor(1);

	m = (TH2F*)gROOT->FindObject("matrix");
	if (m) {m->Delete();}
    m2 = (TH2F*)gROOT->FindObject("matrix2");
    if (m2) {m2->Delete();}
        m3 = (TH2F*)gROOT->FindObject("matrix3");
    if (m3) {m3->Delete();}

	// declarations and stuff
	ifstream  ifile1("../alfna"), ifile2("../fg"), ifile3("/home/fabiobz/progs/RAINIER/Jint_Greg_mama_RIPL_Gg44_4res_04/1Gen.m");
	string line;
	string cal_dummy;
	string dim_dummy;
	char pdf_filename[512];
	int dim;
	int dim_start;
	int dim_stop;
	int dim_size;
	int position;
	int file_length;
	line.resize(200);	// need long enough line to read MAMA headers
	double x_cal[3] = {0.,1.,0.};	// calibration coeffs. on x axis: a0, a1, a2
	double y_cal[3] = {0.,1.,0.};	// calibration coeffs. on y axis: a0, a1, a2
	int dx, dy;	// dimension on x and y axis
	int ix, iy;
	double value;
	double x,y;
	double number_of_counts = 0.;
	double new_y1, new_y2;
	int sign_ycal;


	// open file to read
	if(!ifile1){
		cout << "\n Could not open file!!!\n ";
		exit(1);
	}
	else cout << "\n Successful opening of file"  << endl;


	// read MAMA header (fixed format). The 10 first lines are info text
	if(!getline(ifile1,line) || line.substr(0,10) != "!FILE=Disk"){	// check correct format
		printf("\n This is not a MAMA file!!!\n ");
		exit(2);
	}
	getline(ifile1,line);	// skip !KIND=Spectrum
	getline(ifile1,line);	// skip !LABORATORY=Oslo Cyclotron Laboratory (OCL)
	getline(ifile1,line);	// skip !EXPERIMENT=mama
	getline(ifile1,line);	// skip !COMMENT=Sorted simulated data
	getline(ifile1,line);	// skip !TIME=DATE:    19/11/09 11:47:26
	getline(ifile1,line);	// get line with calibration
	cout << "\n Reading calibration coeffs.:" << endl;
	// calibration on x axis
	cal_dummy = line.substr(20,13);	// position 20, length 13 characters
	if(!(istringstream(cal_dummy) >> x_cal[0])) cout << "Could not convert string to number." << endl;
	else cout << " Calibration coeff. a0 on x axis is: " << x_cal[0] << " keV." << endl;
	cal_dummy = line.substr(34,13);
	if(!(istringstream(cal_dummy) >> x_cal[1])) cout << "Could not convert string to number." << endl;
	else cout << " Calibration coeff. a1 on x axis is: " << x_cal[1] << " keV/ch." << endl;
	cal_dummy = line.substr(48,13);
	if(!(istringstream(cal_dummy) >> x_cal[2])) cout << "Could not convert string to number." << endl;
	else cout << " Calibration coeff. a2 on x axis is: " << x_cal[2] << " (keV/ch)^2." << endl;
	// calibration on y axis
	cal_dummy = line.substr(62,13);
	if(!(istringstream(cal_dummy) >> y_cal[0])) cout << "Could not convert string to number." << endl;
	else cout << " Calibration coeff. a0 on y axis is: " << y_cal[0] << " keV." << endl;
	cal_dummy = line.substr(76,13);
	if(!(istringstream(cal_dummy) >> y_cal[1])) cout << "Could not convert string to number." << endl;
	else cout << " Calibration coeff. a1 on y axis is: " << y_cal[1] << " keV/ch." << endl;
	cal_dummy = line.substr(90,13);
	if(!(istringstream(cal_dummy) >> y_cal[2])) cout << "Could not convert string to number." << endl;
	else cout << " Calibration coeff. a2 on y axis is: " << y_cal[2] << " (keV/ch)^2.\n" << endl;
	getline(ifile1,line);	// skip !PRECISION=16
	getline(ifile1,line);	// get dimension
	// dimension of matrix
	dim_start = line.find_first_of("=") + 1;
	dim_dummy = line.substr(dim_start,1);
	if(!(istringstream(dim_dummy) >> dim)) cout << "Could not convert string to number." << endl;
	else cout << " Dimension of matrix is: " << dim << endl;
	getline(ifile1,line);	// get channels
	// dimension on x axis
	dim_start = line.find_first_of(":") + 1;
	dim_stop = line.find_last_of(",");
	dim_size = dim_stop - dim_start;
	dim_dummy = line.substr(dim_start,dim_size);
	if(!(istringstream(dim_dummy) >> dx)) cout << "Could not convert string to number." << endl;
	else cout << " Dimension on x axis is: " << dx+1 << " ch." << endl;
	dx = dx+1;
	// dimension on y axis
	dim_start = line.find_last_of(":");
	dim_stop = line.find_last_of(")");
	dim_size = dim_stop - dim_start;
	dim_dummy = line.substr(dim_start+1,dim_size-1);
	if(!(istringstream(dim_dummy) >> dy)) cout << "Could not convert string to number." << endl;
	else cout << " Dimension on y axis is: " << dy+1 << " ch." << endl;
	dy = dy+1;

	// Test if negative calibration coeff. on Ex, then invert axis:
	if(y_cal[1] < 0.){
		sign_ycal = -1;
		new_y1 = y_cal[0] + (y_cal[1]*(double) dy);
		new_y2 = y_cal[0];

		y_cal[0] = new_y1;
		y_cal[1] = (-1.)*y_cal[1];
		cout << " New calibration on y axis: y_cal[0] = " << y_cal[0] << ", y_cal[1] = " << y_cal[1] << endl;

	}

    x_cal[0] /= 1000.; // to get MeV instead of keV
    x_cal[1] /= 1000.;
    y_cal[0] /= 1000.; // to get MeV instead of keV
    y_cal[1] /= 1000.;


	// Make histogram
	TH2D *matrix = new TH2D("matrix","",dx,x_cal[0],dx*x_cal[1]+x_cal[0],dy,y_cal[0],dy*y_cal[1]+y_cal[0]);
	matrix->SetOption("colz");
	gStyle->SetPalette(1);


	if(sign_ycal < 0.){	// if negative calibration coeff. on y axis
		for(iy=dy;iy>0;iy--){
			for(ix=0;ix<dx;ix++){
				ifile1 >> value;
				number_of_counts += value;
				matrix->SetBinContent(ix,iy,value);
			}
		}
	}
	else{	// if positive calibration coeff. on y axis
		for(iy=0;iy<dy;iy++){
			for(ix=0;ix<dx;ix++){
				ifile1 >> value;
				number_of_counts += value;
				matrix->SetBinContent(ix,iy,value);
			}
		}
	}

	cout << " F.g. matrix for XXX1 is now filled." << endl;

    // open 90Y file to read
    if(!ifile2){
        cout << "\n Could not open file!!!\n ";
        exit(1);
    }
    else cout << "\n Successful opening of file"  << endl;


    // read MAMA header (fixed format). The 10 first lines are info text
    if(!getline(ifile2,line) || line.substr(0,10) != "!FILE=Disk"){	// check correct format
        printf("\n This is not a MAMA file!!!\n ");
        exit(2);
    }
    getline(ifile2,line);	// skip !KIND=Spectrum
    getline(ifile2,line);	// skip !LABORATORY=Oslo Cyclotron Laboratory (OCL)
    getline(ifile2,line);	// skip !EXPERIMENT=mama
    getline(ifile2,line);	// skip !COMMENT=Sorted simulated data
    getline(ifile2,line);	// skip !TIME=DATE:    19/11/09 11:47:26
    getline(ifile2,line);	// get line with calibration
    cout << "\n Reading calibration coeffs.:" << endl;
    // calibration on x axis
    cal_dummy = line.substr(20,13);	// position 20, length 13 characters
    if(!(istringstream(cal_dummy) >> x_cal[0])) cout << "Could not convert string to number." << endl;
    else cout << " Calibration coeff. a0 on x axis is: " << x_cal[0] << " keV." << endl;
    cal_dummy = line.substr(34,13);
    if(!(istringstream(cal_dummy) >> x_cal[1])) cout << "Could not convert string to number." << endl;
    else cout << " Calibration coeff. a1 on x axis is: " << x_cal[1] << " keV/ch." << endl;
    cal_dummy = line.substr(48,13);
    if(!(istringstream(cal_dummy) >> x_cal[2])) cout << "Could not convert string to number." << endl;
    else cout << " Calibration coeff. a2 on x axis is: " << x_cal[2] << " (keV/ch)^2." << endl;
    // calibration on y axis
    cal_dummy = line.substr(62,13);
    if(!(istringstream(cal_dummy) >> y_cal[0])) cout << "Could not convert string to number." << endl;
    else cout << " Calibration coeff. a0 on y axis is: " << y_cal[0] << " keV." << endl;
    cal_dummy = line.substr(76,13);
    if(!(istringstream(cal_dummy) >> y_cal[1])) cout << "Could not convert string to number." << endl;
    else cout << " Calibration coeff. a1 on y axis is: " << y_cal[1] << " keV/ch." << endl;
    cal_dummy = line.substr(90,13);
    if(!(istringstream(cal_dummy) >> y_cal[2])) cout << "Could not convert string to number." << endl;
    else cout << " Calibration coeff. a2 on y axis is: " << y_cal[2] << " (keV/ch)^2.\n" << endl;
    getline(ifile2,line);	// skip !PRECISION=16
    getline(ifile2,line);	// get dimension
    // dimension of matrix
    dim_start = line.find_first_of("=") + 1;
    dim_dummy = line.substr(dim_start,1);
    if(!(istringstream(dim_dummy) >> dim)) cout << "Could not convert string to number." << endl;
    else cout << " Dimension of matrix is: " << dim << endl;
    getline(ifile2,line);	// get channels
    // dimension on x axis
    dim_start = line.find_first_of(":") + 1;
    dim_stop = line.find_last_of(",");
    dim_size = dim_stop - dim_start;
    dim_dummy = line.substr(dim_start,dim_size);
    if(!(istringstream(dim_dummy) >> dx)) cout << "Could not convert string to number." << endl;
    else cout << " Dimension on x axis is: " << dx+1 << " ch." << endl;
    dx = dx+1;
    // dimension on y axis
    dim_start = line.find_last_of(":");
    dim_stop = line.find_last_of(")");
    dim_size = dim_stop - dim_start;
    dim_dummy = line.substr(dim_start+1,dim_size-1);
    if(!(istringstream(dim_dummy) >> dy)) cout << "Could not convert string to number." << endl;
    else cout << " Dimension on y axis is: " << dy+1 << " ch." << endl;
    dy = dy+1;

    // Test if negative calibration coeff. on Ex, then invert axis:
    if(y_cal[1] < 0.){
        sign_ycal = -1;
        new_y1 = y_cal[0] + (y_cal[1]*(double) dy);
        new_y2 = y_cal[0];

        y_cal[0] = new_y1;
        y_cal[1] = (-1.)*y_cal[1];
        cout << " New calibration on y axis: y_cal[0] = " << y_cal[0] << ", y_cal[1] = " << y_cal[1] << endl;
    }

    x_cal[0] /= 1000.; // to get MeV instead of keV
    x_cal[1] /= 1000.;
    y_cal[0] /= 1000.; // to get MeV instead of keV
    y_cal[1] /= 1000.;

    // Make histogram
    TH2D *matrix2 = new TH2D("matrix2","",dx,x_cal[0],dx*x_cal[1]+x_cal[0],dy,y_cal[0],dy*y_cal[1]+y_cal[0]);
    matrix2->SetOption("colz");
    gStyle->SetPalette(1);


    if(sign_ycal < 0.){	// if negative calibration coeff. on y axis
        for(iy=dy;iy>0;iy--){
            for(ix=0;ix<dx;ix++){
                ifile2 >> value;
                number_of_counts += value;
                matrix2->SetBinContent(ix,iy,value);
            }
        }
    }
    else{	// if positive calibration coeff. on y axis
        for(iy=0;iy<dy;iy++){
            for(ix=0;ix<dx;ix++){
                ifile2 >> value;
                number_of_counts += value;
                matrix2->SetBinContent(ix,iy,value);
            }
        }
    }

    cout << " F.g. matrix for XXX2 is now filled." << endl;



    // open 90Y file to read
    if(!ifile3){
        cout << "\n Could not open file!!!\n ";
        exit(1);
    }
    else cout << "\n Successful opening of file"  << endl;


    // read MAMA header (fixed format). The 10 first lines are info text
    if(!getline(ifile3,line) || line.substr(0,10) != "!FILE=Disk"){ // check correct format
        printf("\n This is not a MAMA file!!!\n ");
        exit(2);
    }
    getline(ifile3,line);   // skip !KIND=Spectrum
    getline(ifile3,line);   // skip !LABORATORY=Oslo Cyclotron Laboratory (OCL)
    getline(ifile3,line);   // skip !EXPERIMENT=mama
    getline(ifile3,line);   // skip !COMMENT=Sorted simulated data
    getline(ifile3,line);   // skip !TIME=DATE:    19/11/09 11:47:26
    getline(ifile3,line);   // get line with calibration
    cout << "\n Reading calibration coeffs.:" << endl;
    // calibration on x axis
    cal_dummy = line.substr(20,13); // position 20, length 13 characters
    if(!(istringstream(cal_dummy) >> x_cal[0])) cout << "Could not convert string to number." << endl;
    else cout << " Calibration coeff. a0 on x axis is: " << x_cal[0] << " keV." << endl;
    cal_dummy = line.substr(34,13);
    if(!(istringstream(cal_dummy) >> x_cal[1])) cout << "Could not convert string to number." << endl;
    else cout << " Calibration coeff. a1 on x axis is: " << x_cal[1] << " keV/ch." << endl;
    cal_dummy = line.substr(48,13);
    if(!(istringstream(cal_dummy) >> x_cal[2])) cout << "Could not convert string to number." << endl;
    else cout << " Calibration coeff. a2 on x axis is: " << x_cal[2] << " (keV/ch)^2." << endl;
    // calibration on y axis
    cal_dummy = line.substr(62,13);
    if(!(istringstream(cal_dummy) >> y_cal[0])) cout << "Could not convert string to number." << endl;
    else cout << " Calibration coeff. a0 on y axis is: " << y_cal[0] << " keV." << endl;
    cal_dummy = line.substr(76,13);
    if(!(istringstream(cal_dummy) >> y_cal[1])) cout << "Could not convert string to number." << endl;
    else cout << " Calibration coeff. a1 on y axis is: " << y_cal[1] << " keV/ch." << endl;
    cal_dummy = line.substr(90,13);
    if(!(istringstream(cal_dummy) >> y_cal[2])) cout << "Could not convert string to number." << endl;
    else cout << " Calibration coeff. a2 on y axis is: " << y_cal[2] << " (keV/ch)^2.\n" << endl;
    getline(ifile3,line);   // skip !PRECISION=16
    getline(ifile3,line);   // get dimension
    // dimension of matrix
    dim_start = line.find_first_of("=") + 1;
    dim_dummy = line.substr(dim_start,1);
    if(!(istringstream(dim_dummy) >> dim)) cout << "Could not convert string to number." << endl;
    else cout << " Dimension of matrix is: " << dim << endl;
    getline(ifile3,line);   // get channels
    // dimension on x axis
    dim_start = line.find_first_of(":") + 1;
    dim_stop = line.find_last_of(",");
    dim_size = dim_stop - dim_start;
    dim_dummy = line.substr(dim_start,dim_size);
    if(!(istringstream(dim_dummy) >> dx)) cout << "Could not convert string to number." << endl;
    else cout << " Dimension on x axis is: " << dx+1 << " ch." << endl;
    dx = dx+1;
    // dimension on y axis
    dim_start = line.find_last_of(":");
    dim_stop = line.find_last_of(")");
    dim_size = dim_stop - dim_start;
    dim_dummy = line.substr(dim_start+1,dim_size-1);
    if(!(istringstream(dim_dummy) >> dy)) cout << "Could not convert string to number." << endl;
    else cout << " Dimension on y axis is: " << dy+1 << " ch." << endl;
    dy = dy+1;

    // Test if negative calibration coeff. on Ex, then invert axis:
    if(y_cal[1] < 0.){
        sign_ycal = -1;
        new_y1 = y_cal[0] + (y_cal[1]*(double) dy);
        new_y2 = y_cal[0];

        y_cal[0] = new_y1;
        y_cal[1] = (-1.)*y_cal[1];
        cout << " New calibration on y axis: y_cal[0] = " << y_cal[0] << ", y_cal[1] = " << y_cal[1] << endl;
    }

    x_cal[0] /= 1000.; // to get MeV instead of keV
    x_cal[1] /= 1000.;
    y_cal[0] /= 1000.; // to get MeV instead of keV
    y_cal[1] /= 1000.;

    // Make histogram
    TH2D *matrix3 = new TH2D("matrix3","",dx,x_cal[0],dx*x_cal[1]+x_cal[0],dy,y_cal[0],dy*y_cal[1]+y_cal[0]);
    matrix3->SetOption("colz");
    // gStyle->SetPalette(1);


    if(sign_ycal < 0.){ // if negative calibration coeff. on y axis
        for(iy=dy;iy>0;iy--){
            for(ix=0;ix<dx;ix++){
                ifile3 >> value;
                number_of_counts += value;
                matrix3->SetBinContent(ix,iy,value);
            }
        }
    }
    else{   // if positive calibration coeff. on y axis
        for(iy=0;iy<dy;iy++){
            for(ix=0;ix<dx;ix++){
                ifile3 >> value;
                number_of_counts += value;
                matrix3->SetBinContent(ix,iy,value);
            }
        }
    }

    cout << " F.g. matrix for XXX3 is now filled." << endl;




    // Create TCanvas
    TCanvas *c1 = new TCanvas("c1","Coincidence spectra",900*2,320*2);
    c1->Divide(3,1,0,0);

    c1->cd(1);
    c1_1->SetLogz();
    c1_1->SetLeftMargin(0.14);
    c1_1->SetRightMargin(0.05);
    c1_1->SetBottomMargin(0.14);
//    c1_1->SetTopMargin(0.09);

    matrix->GetXaxis()->SetTitle(" (a)   #gamma-ray energy E_{#gamma} (MeV)");
    matrix->GetYaxis()->SetTitle(" Excitation energy E_{x} (MeV)");
    matrix->GetZaxis()->SetTitleFont(42);
    matrix->GetXaxis()->SetTitleSize(0.055);
    matrix->GetZaxis()->CenterTitle();
    matrix->GetXaxis()->SetTitleOffset(1.2);
    matrix->GetYaxis()->SetTitleOffset(1.);
    matrix->GetXaxis()->SetTitleFont(42);
    matrix->GetYaxis()->SetTitleFont(42);
    matrix->GetXaxis()->SetLabelFont(42);
    matrix->GetYaxis()->SetLabelFont(42);
    matrix->GetXaxis()->SetTitleSize(0.05);
    matrix->GetYaxis()->SetTitleSize(0.055);
    matrix->GetXaxis()->SetLabelSize(0.05);
    matrix->GetYaxis()->SetLabelSize(0.05);
    matrix->GetZaxis()->SetLabelFont(42);
//    matrix->GetXaxis()->SetRangeUser(0.,12.3);
//    matrix->GetYaxis()->SetRangeUser(0.,12.3);
    matrix->GetXaxis()->SetRangeUser(0,6.95);
    matrix->GetYaxis()->SetRangeUser(0,6.95);
    matrix->GetZaxis()->SetRangeUser(1,3000);
    matrix->Draw("col");

//    pl = new TPaveLabel(0.3,0.9,0.7,1.,"(a) ^{239}Pu(d,p#gamma)^{240}Pu","NDC");
//    pl->SetFillColor(0);
//    pl->SetBorderSize(5);
//    pl->SetTextSize(0.6);
//    pl->SetTextFont(42);
//    pl->Draw();

//dashed lines; here to indicated the first generations margines
// left vertical line
    TLine *line1 = new TLine(1.2,2.55,1.2,4.0);
    line1->SetLineWidth(2);
    line1->SetLineStyle(2);
    line1->Draw();
// lower horizontal (x1, y1, {x2=y1+0.2} , y2)
    TLine *line2 = new TLine(1.2,2.55,2.8,2.55);
    line2->SetLineWidth(2);
    line2->SetLineStyle(2);
    line2->Draw();
// diagonal
    TLine *line3 = new TLine(2.8,2.55,4.0+0.2,4.0);
    line3->SetLineWidth(2);
    line3->SetLineStyle(2);
    line3->Draw();
// upper horizontal
    TLine *line4 = new TLine(1.2,4.0,4.0+0.2,4.0);
    line4->SetLineWidth(2);
    line4->SetLineStyle(2);
    line4->Draw();


    c1->cd(2);
    c1_2->SetLogz();
    c1_2->SetRightMargin(0.07);
    c1_2->SetLeftMargin(0.05);
//    c1_2->SetTopMargin(0.09);
    c1_2->SetBottomMargin(0.14);

    matrix2->GetXaxis()->SetTitle(" (b)   #gamma-ray energy E_{#gamma} (MeV)");
    matrix2->GetXaxis()->SetLabelSize(0.05);
    matrix2->GetXaxis()->SetTitleOffset(1.2);
    matrix2->GetXaxis()->SetTitleSize(0.05);
    matrix2->GetYaxis()->SetLabelSize(0.05);
    matrix2->GetYaxis()->SetTitleSize(0.055);
    //matrix2->GetYaxis()->SetLabelOffset(40.7);
    matrix2->GetXaxis()->SetTitleFont(42);
    matrix2->GetYaxis()->SetTitleFont(42);
    matrix2->GetXaxis()->SetLabelFont(42);
    matrix2->GetYaxis()->SetLabelFont(42);
    matrix2->GetZaxis()->SetLabelFont(42);
    matrix2->GetZaxis()->SetLabelSize(0.053);
//    matrix2->GetXaxis()->SetRangeUser(0.1,9.3);
//    matrix2->GetYaxis()->SetRangeUser(0.,9.3);
    matrix2->GetXaxis()->SetRangeUser(0.1,7);
    matrix2->GetYaxis()->SetRangeUser(0,6.95);
    matrix2->GetZaxis()->SetRangeUser(1,3000);
    matrix2->Draw("col");


//dashed lines; here to indicated the first generations margines
// left vertical line
    // TLine *line1 = new TLine(1.2,2.6,1.2,5);
    // line1->SetLineWidth(2);
    // line1->SetLineStyle(2);
    line1->Draw();
// lower horizontal (x1, y1, {x2=y1+0.2} , y2)
    // TLine *line2 = new TLine(1.2,2.6,2.8,2.6);
    // line2->SetLineWidth(2);
    // line2->SetLineStyle(2);
    line2->Draw();
// diagonal
    // TLine *line3 = new TLine(2.8,2.6,5.2,5);
    // line3->SetLineWidth(2);
    // line3->SetLineStyle(2);
    line3->Draw();
// upper horizontal
    // TLine *line4 = new TLine(1.2,5,5.2,5);
    // line4->SetLineWidth(2);
    // line4->SetLineStyle(2);
    line4->Draw();




    c1->cd(3);
    c1_3->SetLogz();
    c1_3->SetRightMargin(0.07);
    c1_3->SetLeftMargin(0.05);
//    c1_2->SetTopMargin(0.09);
    c1_3->SetBottomMargin(0.14);

    matrix3->GetXaxis()->SetTitle(" (c)   #gamma-ray energy E_{#gamma} (MeV)");
    matrix3->GetXaxis()->SetLabelSize(0.05);
    matrix3->GetXaxis()->SetTitleOffset(1.2);
    matrix3->GetXaxis()->SetTitleSize(0.05);
    matrix3->GetYaxis()->SetLabelSize(0.05);
    matrix3->GetYaxis()->SetTitleSize(0.055);
    //matr3x2->GetYaxis()->SetLabelOffset(40.7);
    matrix3->GetXaxis()->SetTitleFont(42);
    matrix3->GetYaxis()->SetTitleFont(42);
    matrix3->GetXaxis()->SetLabelFont(42);
    matrix3->GetYaxis()->SetLabelFont(42);
    matrix3->GetZaxis()->SetLabelFont(42);
    matrix3->GetZaxis()->SetLabelSize(0.053);
//    matr3x2->GetXaxis()->SetRangeUser(0.1,9.3);
//    matr3x2->GetYaxis()->SetRangeUser(0.,9.3);
    matrix3->GetXaxis()->SetRangeUser(0.1,7);
    matrix3->GetYaxis()->SetRangeUser(0,6.95);
    matrix3->GetZaxis()->SetRangeUser(1,3000);
    matrix2->Scale(10.);
    matrix3->Draw("colz");


//dashed lines; here to indicated the first generations margines
// left vertical line
    // TLine *line1 = new TLine(1.2,2.6,1.2,5);
    // line1->SetLineWidth(2);
    // line1->SetLineStyle(2);
    line1->Draw();
// lower horizontal (x1, y1, {x2=y1+0.2} , y2)
    // TLine *line2 = new TLine(1.2,2.6,2.8,2.6);
    // line2->SetLineWidth(2);
    // line2->SetLineStyle(2);
    line2->Draw();
// diagonal
    // TLine *line3 = new TLine(2.8,2.6,5.2,5);
    // line3->SetLineWidth(2);
    // line3->SetLineStyle(2);
    line3->Draw();
// upper horizontal
//     TLine *line4 = new TLine(1.2,5,5.2,5);
//     line4->SetLineWidth(2);
//     line4->SetLineStyle(2);
    line4->Draw();

//    pl2 = new TPaveLabel(0.3,0.9,0.8,1.,"(b) ^{239}Pu(d,p#gamma)^{240}Pu","NDC");
//    pl2->SetFillColor(0);
//    pl2->SetBorderSize(5);
//    pl2->SetTextSize(0.6);
//    pl2->SetTextFont(42);
//    pl2->Draw();


    gPad->Update();
    // TPaletteAxis *palette = (TPaletteAxis*)matrix2->GetListOfFunctions()->FindObject("palette");
    // if(!palette){cout << "nono." << endl;}
    // palette->SetX1NDC(0.898);
    // palette->SetX2NDC(0.93);
    // palette->SetLabelSize(0.05);
    // palette->SetLabelFont(42);
    // palette->Draw();

    c1->Update();

	// Print to pdf file
//	c1->Print("fg_matrices_yttrium.pdf");
    c1->Print("m_alfna_compare_3_article.png");
    //c1->Print("m_alfna_compare_3.jpg");
    //c1->Print("m_alfna_compare_3.pdf");




}	// END of script
