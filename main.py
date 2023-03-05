#lep_pt = transverse momentum of the lepton,
#lep_eta = pseudo-rapidity of the lepton,
#lep_phi = azimuthal angle of the lepton,
#lep_E = energy of the lepton.

import ROOT, math
from ROOT import TLegend, kRed, kBlue, kFullDotMedium

pi = math.pi
infinity = math.inf
f_low = 80 #Edges for fitting
f_up = 100
bins = 200 #Histogram bins and edges
low = 0
up = 200
leadLepton  = ROOT.TLorentzVector() #Lead and trail lepton as Lorentz Vectors
trailLepton = ROOT.TLorentzVector()

#2lep 13 TeV sample
a = ROOT.TFile.Open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/2lep/Data/data_B.2lep.root")
tree = a.Get("mini") #Getting the data from the .root file
tree.GetEntries()
print('Entries: ' + str(tree.GetEntries()))

#Breit-Wigner plus Gaussian function
Fit = ROOT.TF1("Fit", "[0]*TMath::BreitWigner(x,[1],[2]) + gaus", f_low, f_up) #Predifined Breit-Wigner function
Fit.SetParameters(4000, 90.11, 3.386) #Setting base parameters
Fit.Save(f_low, f_up, 0, 0, 0, 0) #Setting the interval for fitting

#Functions for the histograms, the calculated mass, the different selection cuts, and the event loops
def hist_draw(hist, canvas, color):
    hist.Draw()
    hist.Fit('Fit', "R", "", f_low, f_up) #R or S
    hist.SetFillStyle(3003)
    hist.SetFillColor(color)
    Fit.SetLineColor(kRed)
    canvas.Draw()

def error_hist_draw_2 (error_canvas, error_hist, bin_1, error_1, bin_2, error_2):
    error_hist.SetBinContent(1, bin_1) #Setting the muon center parameter
    error_hist.SetBinError(1, error_1) #Setting the error of the parameter
    error_hist.SetBinContent(2, bin_2) #Setting the electron center parameter
    error_hist.SetBinError(2, error_2) #Setting the error
    error_hist.SetLineWidth(2)
    error_hist_axis = error_hist.GetXaxis() #Getting the x-axis of the histogram
    error_hist_axis.SetBinLabel(1,'Muon Data') #Labeling the first bin
    error_hist_axis.SetBinLabel(2,'Electron Data') #Labeling the second bin
    error_hist.SetMarkerStyle(kFullDotMedium) #Setting the marker style
    error_hist.SetMarkerColor(kBlue+2) #Settting marker color
    error_hist.SetStats(0)
    error_hist.Draw('e1')
    error_canvas.Draw()

def error_hist_draw_pt (error_canvas, error_hist, bin_1, error_1, bin_2, error_2, bin_3, error_3, bin_4, error_4, bin_5, error_5):
    error_hist.SetBinContent(1, bin_1) 
    error_hist.SetBinError(1, error_1) 
    error_hist.SetBinContent(2, bin_2) 
    error_hist.SetBinError(2, error_2) 
    error_hist.SetBinContent(3, bin_3)
    error_hist.SetBinError(3, error_3)
    error_hist.SetBinContent(4, bin_4)
    error_hist.SetBinError(4, error_4)
    error_hist.SetBinContent(5, bin_5)
    error_hist.SetBinError(5, error_5)
    error_hist.SetLineWidth(2)
    error_hist_axis = error_hist.GetXaxis()
    error_hist_axis.SetBinLabel(1, "PT < 30")
    error_hist_axis.SetBinLabel(2, "30 < PT < 40")
    error_hist_axis.SetBinLabel(3, "40 < PT < 50") 
    error_hist_axis.SetBinLabel(4, "50 < PT < 60")
    error_hist_axis.SetBinLabel(5, "PT > 60")
    error_hist.SetMarkerStyle(kFullDotMedium)
    error_hist.SetMarkerColor(kBlue+2)
    error_hist.SetStats(0)
    error_hist.Draw('e1')
    error_canvas.Draw()

def error_hist_draw_eta (error_canvas, error_hist, bin_1, error_1, bin_2, error_2, bin_3, error_3, bin_4, error_4, bin_5, error_5):
    error_hist.SetBinContent(1, bin_1) 
    error_hist.SetBinError(1, error_1) 
    error_hist.SetBinContent(2, bin_2) 
    error_hist.SetBinError(2, error_2) 
    error_hist.SetBinContent(3, bin_3)
    error_hist.SetBinError(3, error_3)
    error_hist.SetBinContent(4, bin_4)
    error_hist.SetBinError(4, error_4)
    error_hist.SetBinContent(5, bin_5)
    error_hist.SetBinError(5, error_5)
    error_hist.SetLineWidth(2)
    error_hist_axis = error_hist.GetXaxis()
    error_hist_axis.SetBinLabel(1, "eta < 0.5")
    error_hist_axis.SetBinLabel(2, "0.5 < eta < 1")
    error_hist_axis.SetBinLabel(3, "1 < eta < 1.5") 
    error_hist_axis.SetBinLabel(4, "1.5 < eta < 2")
    error_hist_axis.SetBinLabel(5, "eta > 2")
    error_hist.SetMarkerStyle(kFullDotMedium)
    error_hist.SetMarkerColor(kBlue+2)
    error_hist.SetStats(0)
    error_hist.Draw('e1')
    error_canvas.Draw()

def InvMass_Hist(hist): #Calculatng, returning and filling the histogram with the invariant mass
    leadLepton.SetPtEtaPhiE(tree.lep_pt[0]/1000., tree.lep_eta[0], tree.lep_phi[0], tree.lep_E[0]/1000.) #Define one TLorentz vector for each lepton; two vectors (devide by 1000 to get value in GeV)
    trailLepton.SetPtEtaPhiE(tree.lep_pt[1]/1000., tree.lep_eta[1], tree.lep_phi[1], tree.lep_E[1]/1000.)
    invmass = leadLepton + trailLepton  #Addition of two TLorentz vectors above
    if 0 < invmass.M() < 200:
        hist.Fill(invmass.M()) #Filling the histogram if the calculated mass is relevant

def pt(type, T_low, T_up, hist_var): #Transverse momentum
    if (tree.lep_n == 2 and tree.lep_charge[0] != tree.lep_charge[1] and tree.lep_type[0] == tree.lep_type[1] == type): #Base conditions
        if (T_low*1000 < tree.lep_pt[0] < T_up*1000 and T_low*1000 < tree.lep_pt[1] < T_up*1000): #Transverse momentum in GeV
            InvMass_Hist(hist_var)

def eta(type, Eta_low, Eta_up, hist_var): #Pseudorapidity
    if (tree.lep_n == 2 and tree.lep_charge[0] != tree.lep_charge[1] and tree.lep_type[0] == tree.lep_type[1] == type): #Base conditions
        if (Eta_low < tree.lep_eta[0] < Eta_up and Eta_low < tree.lep_eta[1] < Eta_up): #Pseudorapidity
            InvMass_Hist(hist_var)

def event_loop(variable, type, min, max, canvas, histogram): #Event loop for the momentum and pseudorapidity
    print(str(histogram))

    n=0
    for event in tree:
        n += 1
        if(n%100000==0):
            print(n)
        variable(type, min, max, histogram)

    hist_draw(histogram, canvas, 4)

def event_loop_channel(type, canvas, histogram): #Event loop for the decay channels
    print(str(histogram))

    n=0
    for event in tree:
        n += 1
        if(n%100000==0):
            print(n)
        if (tree.lep_n == 2 and tree.lep_charge[0] != tree.lep_charge[1] and tree.lep_type[0] == tree.lep_type[1] == type):
            InvMass_Hist(histogram)

    hist_draw(histogram, canvas, 4)


#Muons vs electrons
canvas_muon = ROOT.TCanvas("Canvas_muon","Title",800,600)
hist_muon = ROOT.TH1F("Muon Decay Channel", "; mass [GeV]; events", bins, low, up)
event_loop_channel(13, canvas_muon, hist_muon)

canvas_electron = ROOT.TCanvas("Canvas_electron","Title",800,600)
hist_electron = ROOT.TH1F("Electron Decay Channel", "; mass [GeV]; events", bins, low, up)
event_loop_channel(11, canvas_electron, hist_electron)

#Momentum, muons
canvas_pt_muon_1 = ROOT.TCanvas("Canvas_pt_muon_1","Title",800,600)
hist_pt_muon_1 = ROOT.TH1F("Muon Momentum 1", "; mass [GeV]; events", bins, low, up)
event_loop(pt, 13, 0, 30, canvas_pt_muon_1, hist_pt_muon_1)

canvas_pt_muon_2 = ROOT.TCanvas("Canvas_pt_muon_2","Title",800,600)
hist_pt_muon_2 = ROOT.TH1F("Muon Momentum 2", "; mass [GeV]; events", bins, low, up)
event_loop(pt, 13, 30, 40, canvas_pt_muon_2, hist_pt_muon_2)

canvas_pt_muon_3 = ROOT.TCanvas("Canvas_pt_muon_3","Title",800,600)
hist_pt_muon_3 = ROOT.TH1F("Muon Momentum 3", "; mass [GeV]; events", bins, low, up)
event_loop(pt, 13, 40, 50, canvas_pt_muon_3, hist_pt_muon_3)

canvas_pt_muon_4 = ROOT.TCanvas("Canvas_pt_muon_4","Title",800,600)
hist_pt_muon_4 = ROOT.TH1F("Muon Momentum 4", "; mass [GeV]; events", bins, low, up)
event_loop(pt, 13, 50, 60, canvas_pt_muon_4, hist_pt_muon_4)

canvas_pt_muon_5 = ROOT.TCanvas("Canvas_pt_muon_5","Title",800,600)
hist_pt_muon_5 = ROOT.TH1F("Muon Momentum 5", "; mass [GeV]; events", bins, low, up)
event_loop(pt, 13, 60, infinity, canvas_pt_muon_5, hist_pt_muon_5)

#Momentum, electrons
canvas_pt_electron_1 = ROOT.TCanvas("Canvas_pt_electron_1","Title",800,600)
hist_pt_electron_1 = ROOT.TH1F("Electron Momentum 1", "; mass [GeV]; events", bins, low, up)
event_loop(pt, 11, 0, 30, canvas_pt_electron_1, hist_pt_electron_1)

canvas_pt_electron_2 = ROOT.TCanvas("Canvas_pt_electron_2","Title",800,600)
hist_pt_electron_2 = ROOT.TH1F("Electron Momentum 2", "; mass [GeV]; events", bins, low, up)
event_loop(pt, 11, 30, 40, canvas_pt_electron_2, hist_pt_electron_2)

canvas_pt_electron_3 = ROOT.TCanvas("Canvas_pt_electron_3","Title",800,600)
hist_pt_electron_3 = ROOT.TH1F("Electron Momentum 3", "; mass [GeV]; events", bins, low, up)
event_loop(pt, 11, 40, 50, canvas_pt_electron_3, hist_pt_electron_3)

canvas_pt_electron_4 = ROOT.TCanvas("Canvas_pt_electron_4","Title",800,600)
hist_pt_electron_4 = ROOT.TH1F("Electron Momentum 4", "; mass [GeV]; events", bins, low, up)
event_loop(pt, 11, 50, 60, canvas_pt_electron_4, hist_pt_electron_4)

canvas_pt_electron_5 = ROOT.TCanvas("Canvas_pt_electron_5","Title",800,600)
hist_pt_electron_5 = ROOT.TH1F("Electron Momentum 5", "; mass [GeV]; events", bins, low, up)
event_loop(pt, 11, 60, infinity, canvas_pt_electron_5, hist_pt_electron_5)

#Pseudorapidity, muons
canvas_eta_1 = ROOT.TCanvas("Canvas_eta_1","Title",800,600)
hist_eta_1 = ROOT.TH1F("Pseudorapidity 1", "; mass [GeV]; events", bins, low, up)
event_loop(eta, 13, 0, 0.5, canvas_eta_1, hist_eta_1)

canvas_eta_2 = ROOT.TCanvas("Canvas_eta_2","Title",800,600)
hist_eta_2 = ROOT.TH1F("Pseudorapidity 2", "; mass [GeV]; events", bins, low, up)
event_loop(eta, 13, 0.5, 1, canvas_eta_2, hist_eta_2)

canvas_eta_3 = ROOT.TCanvas("Canvas_eta_3","Title",800,600)
hist_eta_3 = ROOT.TH1F("Pseudorapidity 3", "; mass [GeV]; events", bins, low, up)
event_loop(eta, 13, 1, 1.5, canvas_eta_3, hist_eta_3)

canvas_eta_4 = ROOT.TCanvas("Canvas_eta_4","Title",800,600)
hist_eta_4 = ROOT.TH1F("Pseudorapidity 4", "; mass [GeV]; events", bins, low, up)
event_loop(eta, 13, 1.5, 2, canvas_eta_4, hist_eta_4)

canvas_eta_5 = ROOT.TCanvas("Canvas_eta_5","Title",800,600)
hist_eta_5 = ROOT.TH1F("Pseudorapidity 5", "; mass [GeV]; events", bins, low, up)
event_loop(eta, 13, 2, infinity, canvas_eta_5, hist_eta_5)


#Muons vs electrons, center and width
canvas_channel_center = ROOT.TCanvas('Channel Center','Title',800,600)
hist_channel_center = ROOT.TH1F('Center Parameter','Center Parameter Decay Channels; ; mass [GeV]', 2, 0, 2) #Create histogram for the center parameter
error_hist_draw_2(canvas_channel_center, hist_channel_center, 9.06640e+01, 3.47413e-03, 8.98398e+01, 4.20184e-03)

canvas_channel_width = ROOT.TCanvas('Channel Width','Title',800,600)
hist_channel_width = ROOT.TH1F('Width Parameter','Width Parameter Decay Channels; ; width [GeV]', 2, 0, 2) #Create histogram for the width parameter
error_hist_draw_2(canvas_channel_width, hist_channel_width, 3.27543e+00, 3.68231e-03, 3.67825e+00, 4.12822e-03)

#Momentum, muons, center and width
canvas_muon_pt_center = ROOT.TCanvas('Muon Momentum Center','Title',800,600)
hist_muon_pt_center = ROOT.TH1F('Center Parameter','Center Parameter Muon Momentum; ; mass [GeV]', 5, 0, 2) #Create histogram for the center parameter
error_hist_draw_pt(canvas_muon_pt_center, hist_muon_pt_center, 9.02695e+01, 1.77935e-02, 9.01826e+01, 1.03329e-02, 9.10306e+01, 6.03031e-03, 9.18106e+01, 7.08287e-02, 9.12011e+01, 5.41948e-02)

canvas_muon_pt_width = ROOT.TCanvas('Muon Momentum Width','Title',800,600)
hist_muon_pt_width = ROOT.TH1F('Width Parameter','Width Parameter Muon Momentum; ; width [GeV]', 5, 0, 2) #Create histogram for the width parameter
error_hist_draw_pt(canvas_muon_pt_width, hist_muon_pt_width, 3.26079e+00, 1.88710e-02, 3.20911e+00, 1.07215e-02, 2.80489e+00, 5.67493e-03, 3.49529e+00, 6.96618e-02, 3.72252e+00, 5.29970e-02)

#Momentum, electrons, center and width
canvas_electron_pt_center = ROOT.TCanvas('Electron Momentum Center','Title',800,600)
hist_electron_pt_center = ROOT.TH1F('Center Parameter','Center Parameter Electron Momentum; ; mass [GeV]', 5, 0, 2) #Create histogram for the center parameter
error_hist_draw_pt(canvas_electron_pt_center, hist_electron_pt_center, 8.84283e+01, 2.64766e-02, 8.92109e+01, 1.31931e-02, 9.06716e+01, 6.82766e-03, 9.12653e+01, 6.96478e-02, 9.09279e+01, 3.71773e-02)

canvas_electron_pt_width = ROOT.TCanvas('Electron Momentum Width','Title',800,600)
hist_electron_pt_width = ROOT.TH1F('Width Parameter','Width Parameter Electron Momentum; ; width [GeV]', 5, 0, 2) #Create histogram for the width parameter
error_hist_draw_pt(canvas_electron_pt_width, hist_electron_pt_width, 4.30347e+00, 2.40987e-02, 3.71076e+00, 1.21795e-02, 2.86142e+00, 6.25233e-03, 3.21206e+00, 7.57818e-02, 2.79495e+00, 4.13733e-02)

#Pseudorapidity, muons, center and width
canvas_eta_center = ROOT.TCanvas('Pseudorapidity','Title',800,600)
hist_eta_center = ROOT.TH1F('Center Parameter','Center Parameter Muon Pseudorapidity; ; mass [GeV]', 5, 0, 2) #Create histogram for the center parameter
error_hist_draw_eta(canvas_eta_center, hist_eta_center, 9.06724e+01, 2.65334e-02, 9.06291e+01, 2.79261e-02, 9.05706e+01, 2.63489e-02, 9.06529e+01, 2.90357e-02, 9.05271e+01, 3.05990e-02)

canvas_eta_width = ROOT.TCanvas('Pseudorapidity Width','Title',800,600)
hist_eta_width = ROOT.TH1F('Width Parameter','Width Parameter Muon Pseudorapidity; ; width [GeV]', 5, 0, 2) #Create histogram for the width parameter
error_hist_draw_eta(canvas_eta_width, hist_eta_width, 2.98233e+00, 2.93686e-02, 3.03724e+00, 2.99711e-02, 3.33739e+00, 2.62625e-02, 3.71854e+00, 2.83063e-02, 3.68989e+00, 3.05349e-02)
