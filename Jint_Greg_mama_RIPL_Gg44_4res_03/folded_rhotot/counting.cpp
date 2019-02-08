{
   gROOT->Reset();
   gROOT->SetStyle("Plain");
   gStyle->SetOptTitle(0);
   gStyle->SetOptStat(0);
   gStyle->SetFillColor(0);
   gStyle->SetPadBorderMode(0);
   m = (TH1F*)gROOT->FindObject("h");
   if (m) m->Delete();
   TCanvas *c1 = new TCanvas("c1","Normalization of level density",600,600);
   TH2F *h = new TH2F("h"," ",10,-0.762500,7.037500,50,2.503224,326900000.000000);
   ifstream rholev("rholev.cnt"), rhopaw("rhopaw.cnt"), fermi("fermigas.cnt");
   float levels[71],rho[71],rhoerr[71],energy[1002],energyerr[1002],fermigas[1002];
   float Bn[1]={6.534000};
   float Bnerr[1]={0.001};
   float rho_Bn[1]={32690000.000000};
   float rho_Bnerr[1]={6500000.000000};
   int i = 0;
   float a0 =  -0.7625;
   float a1 =   0.1000;
   float x,y,z;
   while(fermi){
   	fermi >> x;
   	fermigas[i]=x;
   	energy[i]=a0+(a1*i);
   	energyerr[i]=0.0;
      i++;
   }
   i=0;
   while(rhopaw){
   	rhopaw >> y;
   	if(i<70){
   		rho[i]=y;
   	}
   	else{rhoerr[i-70]=y;}
   	i++;
   }
  	i=0;
	while(rholev){
		rholev >> z;
		levels[i]=z;
		i++;
  }
   TGraphErrors *rhoexp = new TGraphErrors(70,energy,rho,energyerr,rhoerr);
   TGraphErrors *rhoBn = new TGraphErrors(1,Bn,rho_Bn,Bnerr,rho_Bnerr);
   TGraph *fermicalc = new TGraph(1001,energy,fermigas);
   TGraph *level = new TGraph(70,energy,levels);
   c1->SetLogy();
   c1->SetLeftMargin(0.14);
   h->GetXaxis()->CenterTitle();
   h->GetXaxis()->SetTitle("Excitation energy E (MeV)");
   h->GetYaxis()->CenterTitle();
   h->GetYaxis()->SetTitleOffset(1.4);
   h->GetYaxis()->SetTitle("Level density #rho (E) (MeV^{-1})");
   h->Draw();
   rhoexp->SetMarkerStyle(21);   rhoexp->SetMarkerSize(0.8);
   rhoexp->Draw("P");
   fermicalc->SetLineStyle(2);
   fermicalc->DrawGraph(40,&fermicalc->GetX()[39],&fermicalc->GetY()[39],"L");
   level->SetLineStyle(1);
   level->Draw("L");
   rhoBn->SetMarkerStyle(25);
   rhoBn->SetMarkerSize(0.8);
   rhoBn->Draw("P");
   TLegend *leg = new TLegend(0.15,0.70,0.6,0.85);
   leg->SetBorderSize(0);
   leg->SetFillColor(0);
   leg->AddEntry(rhoexp," Oslo data ","P");
   leg->AddEntry(level," Known levels ","L");
   leg->AddEntry(fermicalc," CT or FG model ","L");	
   leg->AddEntry(rhoBn," #rho from neutron res. data ","P");
   leg->Draw();
   TLatex t;
   t.SetTextSize(0.05);
   t.DrawLatex(    5.630,1.634e+08,"^{xx}Yy");
   TArrow *arrow1 = new TArrow(0.437500,422.777688,0.437500,59.521049,0.02,">");
   arrow1->Draw();
   TArrow *arrow2 = new TArrow(0.737500,1078.097158,0.737500,151.780655,0.02,">");
   arrow2->Draw();
   TArrow *arrow3 = new TArrow(3.237500,520108.115896,3.237500,73223.781250,0.02,">");
   arrow3->Draw();
   TArrow *arrow4 = new TArrow(4.737500,19781731.377345,4.737500,2784984.750000,0.02,">");
   arrow4->Draw();
   c1->Update();
   c1->Print("counting.pdf");
   c1->Print("counting.eps");
   c1->Print("counting.ps");
}
