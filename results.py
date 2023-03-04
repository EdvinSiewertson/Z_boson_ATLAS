import ROOT, math
from ROOT import TLegend, kRed, kBlue, kFullDotMedium

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
    error_hist.Draw('e1')
    error_canvas.Draw()
    
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
