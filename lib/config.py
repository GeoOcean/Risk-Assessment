import matplotlib.pyplot as plt

# warnings
import warnings
warnings.filterwarnings("ignore")

# plt.style.use('seaborn')
plt.rcParams['figure.dpi'] = 150

colors = ['#5052F8', '#E83D2E', '#1AC484', '#9943F9', '#FE8E48']
code_crs_samoa = 32702

# Samoa config
code = 32702
region = [-22, 185, 10, 10] # Lat, lon , dy, dx
extend_upolu = [370000, 460000, 8440000, 8480000]
