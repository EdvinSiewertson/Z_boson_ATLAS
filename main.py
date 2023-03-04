#lep_pt = transverse momentum of the lepton,
#lep_eta = pseudo-rapidity of the lepton,
#lep_phi = azimuthal angle of the lepton,
#lep_E = energy of the lepton.

import ROOT, math
from ROOT import TLegend, kRed, kBlue

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
event_loop(pt, 13, 0, 30, canvas_pt_electron_1, hist_pt_electron_1)

canvas_pt_electron_2 = ROOT.TCanvas("Canvas_pt_electron_2","Title",800,600)
hist_pt_electron_2 = ROOT.TH1F("Electron Momentum 2", "; mass [GeV]; events", bins, low, up)
event_loop(pt, 13, 30, 40, canvas_pt_electron_2, hist_pt_electron_2)

canvas_pt_electron_3 = ROOT.TCanvas("Canvas_pt_electron_3","Title",800,600)
hist_pt_electron_3 = ROOT.TH1F("Electron Momentum 3", "; mass [GeV]; events", bins, low, up)
event_loop(pt, 13, 40, 50, canvas_pt_electron_3, hist_pt_electron_3)

canvas_pt_electron_4 = ROOT.TCanvas("Canvas_pt_electron_4","Title",800,600)
hist_pt_electron_4 = ROOT.TH1F("Electron Momentum 4", "; mass [GeV]; events", bins, low, up)
event_loop(pt, 13, 50, 60, canvas_pt_electron_4, hist_pt_electron_4)

canvas_pt_electron_5 = ROOT.TCanvas("Canvas_pt_electron_5","Title",800,600)
hist_pt_electron_5 = ROOT.TH1F("Electron Momentum 5", "; mass [GeV]; events", bins, low, up)
event_loop(pt, 13, 60, infinity, canvas_pt_electron_5, hist_pt_electron_5)

#Pseudorapidity
canvas_eta_1 = ROOT.TCanvas("Canvas_eta_1","Title",800,600)
hist_eta_1 = ROOT.TH1F("Pseudorapidity 1", "; mass [GeV]; events", bins, low, up)
event_loop(eta, 13, 30, 60, canvas_eta_1, hist_eta_1)

canvas_eta_2 = ROOT.TCanvas("Canvas_eta_2","Title",800,600)
hist_eta_2 = ROOT.TH1F("Pseudorapidity 2", "; mass [GeV]; events", bins, low, up)
event_loop(eta, 13, 30, 60, canvas_eta_2, hist_eta_2)

canvas_eta_3 = ROOT.TCanvas("Canvas_eta_3","Title",800,600)
hist_eta_3 = ROOT.TH1F("Pseudorapidity 3", "; mass [GeV]; events", bins, low, up)
event_loop(eta, 13, 30, 60, canvas_eta_3, hist_eta_3)

canvas_eta_4 = ROOT.TCanvas("Canvas_eta_4","Title",800,600)
hist_eta_4 = ROOT.TH1F("Pseudorapidity 4", "; mass [GeV]; events", bins, low, up)
event_loop(eta, 13, 30, 60, canvas_eta_4, hist_eta_4)

canvas_eta_5 = ROOT.TCanvas("Canvas_eta_5","Title",800,600)
hist_eta_5 = ROOT.TH1F("Pseudorapidity 5", "; mass [GeV]; events", bins, low, up)
event_loop(eta, 13, 30, 60, canvas_eta_5, hist_eta_5)
