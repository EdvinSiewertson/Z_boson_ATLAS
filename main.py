"""lep_pt = transverse momentum of the lepton,
lep_eta = pseudorapidity of the lepton,
lep_phi = azimuthal angle of the lepton,
lep_E = energy of the lepton."""

from ROOT import TFile, TLorentzVector, TF1, TH1F, TCanvas, kRed, kBlue, kFullDotMedium
from math import inf

f_low = 80 # Edges for fitting
f_up = 100
bins = 200 # Histogram bins and edges
low = 0
up = 200
leadLepton  = TLorentzVector() # Lead and trail lepton as Lorentz Vectors
trailLepton = TLorentzVector()

# 2lep 13 TeV sample
data_file = TFile.Open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/2lep/Data/data_B.2lep.root")
tree = data_file.Get("mini") # Getting the data from the .root file
tree.GetEntries()
print(f"Entries: {tree.GetEntries()}")

# Breit-Wigner plus Gaussian function
Fit = TF1("Fit", "[0] * TMath::BreitWigner(x, [1], [2]) + gaus", f_low, f_up) #Predifined Breit-Wigner function
Fit.SetParameters(4000, 90.11, 3.386) #Setting base parameters
Fit.Save(f_low, f_up, 0, 0, 0, 0) #Setting the interval for fitting

# Functions for the histograms, the calculated mass, the different selection cuts, the event loops etc.
def create_canvas_and_hist(name, title):
    canvas = TCanvas(name, title, 800, 600)
    hist = TH1F(title, "; mass [GeV]; events", bins, low, up)
    return canvas, hist

def hist_draw(hist, canvas, color):
    hist.Draw()
    hist.Fit('Fit', "R", "", f_low, f_up) #R or S
    hist.SetFillStyle(3003)
    hist.SetFillColor(color)
    Fit.SetLineColor(kRed)
    canvas.Draw()

def InvMass_Hist(hist): # Calculatng, returning and filling the histogram with the invariant mass
    leadLepton.SetPtEtaPhiE(tree.lep_pt[0]/1000., tree.lep_eta[0], tree.lep_phi[0], tree.lep_E[0]/1000.) # Define one TLorentz vector for each lepton; two vectors (devide by 1000 to get value in GeV)
    trailLepton.SetPtEtaPhiE(tree.lep_pt[1]/1000., tree.lep_eta[1], tree.lep_phi[1], tree.lep_E[1]/1000.)
    invmass = leadLepton + trailLepton # Addition of two TLorentz vectors above
    if 0 < invmass.M() < 200:
        hist.Fill(invmass.M()) # Filling the histogram if the calculated mass is relevant

def pt(type, T_low, T_up, hist_var): # Transverse momentum
    if (tree.lep_n == 2 and tree.lep_charge[0] != tree.lep_charge[1] and tree.lep_type[0] == tree.lep_type[1] == type): # Base conditions
        if (T_low*1000 < tree.lep_pt[0] < T_up*1000 and T_low*1000 < tree.lep_pt[1] < T_up*1000): # Transverse momentum in GeV
            InvMass_Hist(hist_var)

def eta(type, Eta_low, Eta_up, hist_var): # Pseudorapidity
    if (tree.lep_n == 2 and tree.lep_charge[0] != tree.lep_charge[1] and tree.lep_type[0] == tree.lep_type[1] == type): # Base conditions
        if (Eta_low < tree.lep_eta[0] < Eta_up and Eta_low < tree.lep_eta[1] < Eta_up): # Pseudorapidity
            InvMass_Hist(hist_var)

def event_loop(variable, type, min, max, canvas, histogram): # Event loop for the momentum and pseudorapidity
    print(str(histogram))

    n=0
    for event in tree:
        n += 1
        if(n%100000==0):
            print(n)
        variable(type, min, max, histogram)

    hist_draw(histogram, canvas, 4)

def event_loop_channel(type, canvas, histogram): # Event loop for the decay channels
    print(str(histogram))
    n=0
    for event in tree:
        n += 1
        if(n%100000==0):
            print(n)
        if (tree.lep_n == 2 and tree.lep_charge[0] != tree.lep_charge[1] and tree.lep_type[0] == tree.lep_type[1] == type):
            InvMass_Hist(histogram)
    hist_draw(histogram, canvas, 4)

# Muon decay channel
canvas_muon, hist_muon = create_canvas_and_hist("Canvas_muon", "Muon Decay Channel")
event_loop_channel(13, canvas_muon, hist_muon)

# Electron decay channel
canvas_electron, hist_electron = create_canvas_and_hist("Canvas_electron", "Electron Decay Channel")
event_loop_channel(11, canvas_electron, hist_electron)

# Muon momentum
muon_ranges = [(0, 30), (30, 40), (40, 50), (50, 60), (60, inf)]
muon_canvases = []
muon_histograms = []

for i, (pt_min, pt_max) in enumerate(muon_ranges):
    canvas, hist = create_canvas_and_hist(f"Canvas_pt_muon_{i+1}", f"Muon Momentum {i+1}")
    event_loop(pt, 13, pt_min, pt_max, canvas, hist)
    muon_canvases.append(canvas)
    muon_histograms.append(hist)

# Electron momentum
electron_ranges = [(0, 30), (30, 40), (40, 50), (50, 60), (60, inf)]
electron_canvases = []
electron_histograms = []

for i, (pt_min, pt_max) in enumerate(electron_ranges):
    canvas, hist = create_canvas_and_hist(f"Canvas_pt_electron_{i+1}", f"Electron Momentum {i+1}")
    event_loop(pt, 11, pt_min, pt_max, canvas, hist)
    electron_canvases.append(canvas)
    electron_histograms.append(hist)

# Pseudorapidity
eta_ranges = [(0, 0.5), (0.5, 1), (1, 1.5), (1.5, 2), (2, inf)]
eta_canvases = []
eta_histograms = []

for i, (eta_min, eta_max) in enumerate(eta_ranges):
    canvas, hist = create_canvas_and_hist(f"Canvas_eta_{i+1}", f"Pseudorapidity {i+1}")
    event_loop(eta, 13, eta_min, eta_max, canvas, hist)
    eta_canvases.append(canvas)
    eta_histograms.append(hist)

#Functions for the center and width histograms
def error_hist_draw_2 (error_canvas, error_hist, bin_1, error_1, bin_2, error_2):
    error_hist.SetBinContent(1, bin_1) # Setting the muon center parameter
    error_hist.SetBinError(1, error_1) # Setting the error of the parameter
    error_hist.SetBinContent(2, bin_2) # Setting the electron center parameter
    error_hist.SetBinError(2, error_2) # Setting the error
    error_hist.SetLineWidth(2)
    error_hist_axis = error_hist.GetXaxis() # Getting the x-axis of the histogram
    error_hist_axis.SetBinLabel(1,'Muon Data') # Labeling the first bin
    error_hist_axis.SetBinLabel(2,'Electron Data') # Labeling the second bin
    error_hist.SetMarkerStyle(kFullDotMedium) # Setting the marker style
    error_hist.SetMarkerColor(kBlue+2) # Settting marker color
    error_hist.SetStats(0)
    error_hist.Draw('e1')
    error_canvas.Draw()

def error_hist_draw_5 (variable, error_canvas, error_hist, bin_1, error_1, bin_2, error_2, bin_3, error_3, bin_4, error_4, bin_5, error_5):
    for i in range(1,6):
        error_hist.SetBinContent(i, locals()['bin_'+str(i)])
        error_hist.SetBinError(i, locals()['error_'+str(i)]) 
    if (variable == "pt"):
        bin_labels = ["PT < 30", "30 < PT < 40", "40 < PT < 50", "50 < PT < 60", "PT > 60"]
        error_hist_axis = error_hist.GetXaxis()
        [error_hist_axis.SetBinLabel(i+1, label) for i, label in enumerate(bin_labels)]
    elif (variable == "eta"):
        bin_labels = ["eta < 0.5", "0.5 < eta < 1", "1 < eta < 1.5", "1.5 < eta < 2", "eta > 2"]
        error_hist_axis = error_hist.GetXaxis()
        [error_hist_axis.SetBinLabel(i+1, label) for i, label in enumerate(bin_labels)]

    error_hist.SetLineWidth(2)
    error_hist.SetMarkerStyle(kFullDotMedium)
    error_hist.SetMarkerColor(kBlue+2)
    error_hist.SetStats(0)
    error_hist.Draw('e1')
    error_canvas.Draw()

def parameter(hist, n): # hist <=> interval. n: 1 = center, 2 = width
    return hist.GetFunction('Fit').GetParameter(n)

def parameter_error(hist, n):
    return hist.GetFunction('Fit').GetParError(n)

def create_center_hist(name, n_bins):
    canvas_center = TCanvas(name + "Center",'Title',800,600)
    hist_center = TH1F('Center Parameter',"Center Parameter" + name + "; ; mass [GeV]", n_bins, 0, 2) # Create histogram for the center parameter
    return canvas_center, hist_center

def create_width_hist(name, n_bins):
    canvas_center = TCanvas(name + "Center",'Title',800,600)
    hist_center = TH1F('Center Parameter',"Center Parameter" + name + "; ; mass [GeV]", n_bins, 0, 2) # Create histogram for the center parameter
    return canvas_center, hist_center

def draw_center(sort, canvas_center, hist_center, *histograms):
    centers = []
    center_errors = []
    for hist in histograms:
        center = parameter(hist, 1)
        center_error = parameter_error(hist, 1)
        centers.append(center)
        center_errors.append(center_error)

    if (sort == "pt" or sort == "eta"):
         error_hist_draw_5(sort, canvas_center, hist_center, *centers, *center_errors)
    else:
        # Draw the histograms with their center points and error bars
        error_hist_draw_2(canvas_center, hist_center, *centers, *center_errors)

def draw_width(sort, canvas_width, hist_width, *histograms):
    widths = []
    width_errors = []
    for hist in histograms:
        width = parameter(hist, 2)
        width_error = parameter_error(hist, 2)
        widths.append(width)
        width_errors.append(width_error)

    if (sort == "pt" or sort == "eta"):
         error_hist_draw_5(sort, canvas_width, hist_width, *widths, *width_errors)
    else:
        # Draw the histograms with their width points and error bars
        error_hist_draw_2(canvas_width, hist_width, *widths, *width_errors)

# Muon and electron center and width parameters histograms
canvas_center, hist_center = create_center_hist("Decay Channels", 2)
draw_center("channel", canvas_center, hist_center, hist_muon, hist_electron)
canvas_width, hist_width = create_width_hist("Decay Channels", 2)
draw_width("channel", canvas_width, hist_width, hist_muon, hist_electron)

# Muon momentum center and width parameters histograms
canvas_center_muon_pt, hist_center_muon_pt = create_center_hist("Muon Transverse Momentum", 5)
draw_center("pt", canvas_center_muon_pt, hist_center_muon_pt, muon_histograms[0], muon_histograms[1], muon_histograms[2], muon_histograms[3], muon_histograms[4])
canvas_width_muon_pt, hist_width_muon_pt = create_width_hist("Muon Transverse Momentum", 5)
draw_width("pt", canvas_width_muon_pt, hist_width_muon_pt, muon_histograms[0], muon_histograms[1], muon_histograms[2], muon_histograms[3], muon_histograms[4])

# Electron momentum center and width parameters histograms
canvas_center_electron_pt, hist_center_electron_pt = create_center_hist("Muon Transverse Momentum", 2)
draw_center("pt", canvas_center_electron_pt, hist_center_electron_pt, electron_histograms[0], electron_histograms[1], electron_histograms[2], electron_histograms[3], electron_histograms[4])
canvas_width_electron_pt, hist_width_electron_pt = create_width_hist("Muon Transverse Momentun", 5)
draw_width("pt", canvas_width_electron_pt, hist_width_electron_pt, electron_histograms[0], electron_histograms[1], electron_histograms[2], electron_histograms[3], electron_histograms[4])

# Muon pseudorapidity center and width parameters histograms
canvas_center_eta, hist_center_eta = create_center_hist("Muon Pseudorapidity", 5)
draw_center("eta", canvas_center_eta, hist_center_eta, eta_histograms[0], eta_histograms[1], eta_histograms[2], eta_histograms[3], eta_histograms[4])
canvas_width_eta, hist_width_eta = create_width_hist("Muon Pseudorapidity ", 5)
draw_width("eta", canvas_width_eta, hist_width_eta, eta_histograms[0], eta_histograms[1], eta_histograms[2], eta_histograms[3], eta_histograms[4])
