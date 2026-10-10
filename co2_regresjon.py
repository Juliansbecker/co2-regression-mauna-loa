#Innlevering matte 2000 datasett


# starter med å gjøre om datasettet til .csv fil og benytter meg av pandas


# importerer nødvendige pakker
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#lager et dataframe i pandas
df = pd.read_csv("data.csv")

# OPPGAVE 1a

#plotter punktene og navngir akser
fig, plott = plt.subplots()
plott.plot(df["x"], df["y"], "o")
plott.set_xlabel("Tid (år etter 1. jan 2022)")
plott.set_ylabel("Konsentrasjon (parts per million)")
plt.grid("visible")



# OPPGAVE 1b - minste kvadraters metode


#regner ut x_gjennomsnitt og y_gjennomsnitt

x_mean = sum(df["x"]) / len(df)
y_mean = sum(df["y"]) / len(df)

#regner ut b  med flere steg:

teller = sum((df["x"] - x_mean) * (df["y"] - y_mean))
nevner = sum((df["x"] - x_mean)**2)
b = teller / nevner
#regner ut a

a = y_mean - b * x_mean


#bruker f streng og printer funksjon y = a + bx

print(f"y = {a:.4f} + {b:.4f}x")
plott.plot(df["x"], a + b*df["x"], "-")     # plotter funksjonen y =  a + bx




#oppgave 1e
#starter med å velge verdier for parameterene og definere S(a,b,c,d,f)




a0 = a #bruker samme som i oppgave b

b0 = b #bruker samme som i oppgave b

c0 = 3 #bruker amplitude = 3, antatt fra å lese av plottet

d0 = 2*np.pi #periode på 1år gir d = 2pi fra ligning i oppgave c

f0 = 0 # faseforskyvningen var ukjent, så startet med 0. Metoden fant f = -0.610

lamd = 0.00001 # testet fra 0.1 og nedover. For store verdier divergerte, 1e-5 konvergerte

h = 0.001 # testet 0.1 til 0.0001. Parameterne var like på tre desimaler for h <= 0.001

N = 10000 # iterasjoner brukt i forløkka, testet 10 til 10 000. Parameterne stabiliserte seg, og 100 000 var for tregt

#gjør om x og y til numpy array

x = df["x"].to_numpy()
y = df["y"].to_numpy()

def F(x,a,b,c,d,f):
    return a + b*x + c*np.sin(d*x + f)

def S(a, b, c, d, f):
    total = 0
    for i in range(len(x)):
        total += (y[i] - a - b*x[i] - c*np.sin(d*x[i] + f))**2
    return total 

#regner ut partiell deriverte for hver parameter med midtpunktsformelen

def dSda(a,b,c,d,f):
    return (S(a+h,b,c,d,f) - S(a-h,b,c,d,f)) / (2*h) 

def dSdb(a, b, c, d, f):
    return (S(a, b+h, c, d, f) - S(a, b-h, c, d, f)) / (2*h)

def dSdc(a, b, c, d, f):
    return (S(a, b, c+h, d, f) - S(a, b, c-h, d, f)) / (2*h)

def dSdd(a, b, c, d, f):
    return (S(a, b, c, d+h, f) - S(a, b, c, d-h, f)) / (2*h)

def dSdf(a, b, c, d, f):
    return (S(a, b, c, d, f+h) - S(a, b, c, d, f-h)) / (2*h)
    

# startverdier
a_gammel = a0
b_gammel = b0
c_gammel = c0
d_gammel = d0
f_gammel = f0

for n in range(N):
    # nye verdier: ny = gammel - lambda · derivert (regnet med de gamle verdiene)
    a_ny = a_gammel - lamd*dSda(a_gammel, b_gammel, c_gammel, d_gammel, f_gammel)
    b_ny = b_gammel - lamd*dSdb(a_gammel, b_gammel, c_gammel, d_gammel, f_gammel)
    c_ny = c_gammel - lamd*dSdc(a_gammel, b_gammel, c_gammel, d_gammel, f_gammel)
    d_ny = d_gammel - lamd*dSdd(a_gammel, b_gammel, c_gammel, d_gammel, f_gammel)
    f_ny = f_gammel - lamd*dSdf(a_gammel, b_gammel, c_gammel, d_gammel, f_gammel)

    # de nye verdiene blir de gamle i neste runde
    a_gammel = a_ny
    b_gammel = b_ny
    c_gammel = c_ny
    d_gammel = d_ny
    f_gammel = f_ny
    

#printer ut F(x) med f-streng
print(f"F(x) = {a_ny:.3f} + {b_ny:.3f}x + {c_ny:.3f}sin({d_ny:.3f}x + {f_ny:.3f})")


# OPPGAVE 1f - plotter F(x) sammen med datapunktene og regresjonslinja
x_plot = np.linspace(min(x), max(x), 1000)   # mange punkter gir en glatt sinuskurve
plott.plot(x_plot, F(x_plot, a_ny, b_ny, c_ny, d_ny, f_ny), "-", label="F(x)")
plott.legend()
fig.savefig("figurer/modell.png", dpi=150)
plt.show()


# OPPGAVE 1h - prediksjon for 2027 og verdi for nyttår 2026
print(f"Prediksjon nyttår 2026/2027: {F(5, a_ny, b_ny, c_ny, d_ny, f_ny):.1f} ppm")

x_2027 = np.linspace(5, 6, 1000)

fig3, ax3 = plt.subplots()
ax3.plot(x_2027, F(x_2027, a_ny, b_ny, c_ny, d_ny, f_ny), "-", label="Prediksjon 2027")
ax3.set_xlabel("Tid (år etter 1. jan 2022)")
ax3.set_ylabel("Konsentrasjon (ppm)")
ax3.set_title("Estimert CO$_2$-konsentrasjon på Mauna Loa i 2027")
ax3.grid(True)
ax3.legend()
fig3.savefig("figurer/prognose_2027.png", dpi=150)
plt.show()


