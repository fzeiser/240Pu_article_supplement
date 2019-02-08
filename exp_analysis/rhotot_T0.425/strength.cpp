{
	gROOT->Reset();
	gROOT->SetStyle("Plain");
	gStyle->SetOptTitle(0);
	gStyle->SetOptStat(0);
	gStyle->SetFillColor(0);
	gStyle->SetPadBorderMode(0);
	m = (TH1F*)gROOT->FindObject("h");
	if (m) m->Delete();
	TCanvas *c1 = new TCanvas("c1","Gamma-ray strength function",600,600);
	TH2F *h = new TH2F("h"," ",10,0.0,   4.679,10,3.026e-09,1.835e-06);
	ifstream strengthfile("strength.nrm");
	float strength[39],strengtherr[39],energyerr[39];
	float energy[381],trans[381];
	int i = 0;
   float a0 =  -0.8296;
   float a1 =   0.1354;
	float x;	
	while(strengthfile){
		strengthfile >> x;
		if(i<38){
			strength[i] = x;
			energy[i] = a0 + (a1*i);
			energyerr[i] = 0.0;
		}	
		else{strengtherr[i-38] = x;}
		i++;
	}
	TGraphErrors *strengthexp = new TGraphErrors(39,energy,strength,energyerr,strengtherr);
    i = 0;
    ifstream transfile("transext.nrm");
    while(transfile){
        transfile >> x;
        energy[i] = a0 + (a1*i);
        trans[i] = x/(2.*3.14*energy[i]*energy[i]*energy[i]);
        i++;
    }
    TGraph *rsfext = new TGraph(i,energy,trans);
	c1->SetLogy();
	c1->SetLeftMargin(0.14);
	h->GetXaxis()->CenterTitle();
	h->GetXaxis()->SetTitle("#gamma-ray energy E_{#gamma} (MeV)");
	h->GetYaxis()->CenterTitle();
	h->GetYaxis()->SetTitleOffset(1.4);
	h->GetYaxis()->SetTitle("#gamma-ray strength function (MeV^{-3})");
	h->Draw();
	strengthexp->SetMarkerStyle(21);
	strengthexp->SetMarkerSize(0.8);
	strengthexp->Draw("P");
    rsfext->SetLineColor(4);
    rsfext->SetLineWidth(2);
    rsfext->Draw("L");
	TLatex t;
	t.SetTextSize(0.05);
	t.DrawLatex(    0.836,5.504e-07,"^{xx}Yy");
	c1->Update();
	c1->Print("strength.pdf");
	c1->Print("strength.eps");
	c1->Print("strength.ps");
}
