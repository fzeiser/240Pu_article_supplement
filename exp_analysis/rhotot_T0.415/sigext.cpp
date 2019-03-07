{
   gROOT->Reset();
   gROOT->SetStyle("Plain");
   gStyle->SetOptTitle(0);
   gStyle->SetOptStat(0);
   gStyle->SetFillColor(0);
   gStyle->SetPadBorderMode(0);
   m = (TH1F*)gROOT->FindObject("h");
   if (m) m->Delete();
   TCanvas *c1 = new TCanvas("c1","Normalization of gamma-transmission coefficient",600,600);
   TH2F *h = new TH2F("h"," ",10,-0.829600,   5.179,50,6.303e+00,8.199e+05);
   ifstream sigfile("sigpaw.cnt");
   float sig[39],sigerr[39];
   float energy[148],energyerr[148];
   float extL[149],extH[149];
   int i;
   float a0 = -0.8296;
   float a1 =  0.1354;
   for(i = 0; i < 59; i++){
   	energy[i] = a0 + (a1*i);
   	energyerr[i] = 0.0;
   	extL[i] = 0.0;
   	extH[i] = 0.0;
   }
   float x, y;
   i = 0;
   while(sigfile){
   	sigfile >> x;
   	if(i<38){
   		sig[i]=x;
   	}
   	else{sigerr[i-38]=x;}
   	i++;
   }
   ifstream extendfile("extendLH.cnt");
   i = 0;
   while(extendfile){
   	extendfile >> x >> y ;
   	extL[i]=x;
   	extH[i]=y;
   	i++;
   }
   TGraph *extLgraph = new TGraph(59,energy,extL);
   TGraph *extHgraph = new TGraph(59,energy,extH);
   TGraphErrors *sigexp = new TGraphErrors(38,energy,sig,energyerr,sigerr);
   c1->SetLogy();
   c1->SetLeftMargin(0.14);
   h->GetXaxis()->CenterTitle();
   h->GetXaxis()->SetTitle("#gamma-ray energy E_{#gamma} (MeV)");
   h->GetYaxis()->CenterTitle();
   h->GetYaxis()->SetTitleOffset(1.4);
   h->GetYaxis()->SetTitle("Transmission coeff. (arb. units)");
   h->Draw();
   sigexp->SetMarkerStyle(21);
   sigexp->SetMarkerSize(0.8);
   sigexp->Draw("P");
   extLgraph->SetLineStyle(1);
   extLgraph->DrawGraph(19,&extLgraph->GetX()[0],&extLgraph->GetY()[0],"L");
   extHgraph->SetLineStyle(1);
   extHgraph->DrawGraph(25,&extHgraph->GetX()[34],&extHgraph->GetY()[34],"L");
   TArrow *arrow1 = new TArrow(1.336e+00,1.125e+03,1.336e+00,2.882e+02,0.02,">");
   arrow1->Draw();
   TArrow *arrow2 = new TArrow(1.607e+00,3.073e+03,1.607e+00,7.875e+02,0.02,">");
   arrow2->Draw();
   TArrow *arrow3 = new TArrow(3.773e+00,1.108e+05,3.773e+00,2.838e+04,0.02,">");
   arrow3->Draw();
   TArrow *arrow4 = new TArrow(4.043e+00,1.602e+05,4.043e+00,4.104e+04,0.02,">");
   arrow4->Draw();
   c1->Update();
   c1->Print("sigext.pdf");
   c1->Print("sigext.eps");
   c1->Print("sigext.ps");
}
