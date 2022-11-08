import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

df = pd.read_excel("D:/Gizem Nalbant/datasets/ab_testing.xlsx")
df.head()

# Impression - Reklam görüntüleme sayısı
# Click - Görüntülenen reklama tıklama sayısı
# Purchase - Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning - Satın alınan ürünler sonrası elde edilen kazanç

### Görev 1:  Veriyi Hazırlama ve Analiz Etme

# Adım 1:  ab_testing_data.xlsxadlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.
#Adım 2: Kontrol ve test grubu verilerini analiz ediniz.

control_group = pd.read_excel("D:/Gizem Nalbant/datasets/ab_testing.xlsx",sheet_name="Control Group")
control_group.head()
control_group.describe().T
control_group.info
control_group.shape
control_group.isnull().sum()
test_group = pd.read_excel("D:/Gizem Nalbant/datasets/ab_testing.xlsx",sheet_name="Test Group")
test_group.head()
test_group.describe().T
test_group.info
test_group.shape
test_group.isnull().sum()

#Adım 3: Analiz işleminden sonra concatmetodunu kullanarak kontrol ve test grubu verilerini birleştiriniz. Görev 1:  Veriyi Hazırlama ve Analiz Etme
df_=pd.concat([control_group, test_group])

#Görev 2:  A/B Testinin Hipotezinin Tanımlanması

#Adım 1: Hipotezi tanımlayınız. H0 : M1 = M2 H1 : M1!= M2
#Adım 2: Kontrol ve test grubu için purchase(kazanç) ortalamalarını analiz ediniz.Görev 2:  A/B Testinin Hipotezinin Tanımlanması

# kontrol grubu kazanç ortalamaları ile test grubu kazanç ortalamaları eşit mi diye bakalım.

control_group["Purchase"].mean() #Out[23]: 550.8940587702316
test_group["Purchase"].mean() #Out[24]: 582.1060966484675

# Aralarında fark var.Bu fark tesadüfi mi diye bakacağız.

#Görev 3:  Hipotez Testinin Gerçekleştirilmesi
# Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.
# Bunlar Normallik Varsayımıve VaryansHomojenliğidir. Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz.

#Normallik varsayımı
#control grup nromallik testi
test_stat, pvalue = shapiro(control_group["Purchase"]) # shapiro bir değişkenin dağılımının normal olup olmadığını test eder.
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#Sonuç :Test Stat = 0.9773, p-value = 0.5891  > 0.05

test_stat, pvalue = shapiro(test_group["Purchase"]) # shapiro bir değişkenin dağılımının normal olup olmadığını test eder.
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#Sonuç : Test Stat = 0.9589, p-value = 0.1541 > 0.05

# Normallik testi reddedilemez.

test_stat, pvalue = levene(control_group["Purchase"],
                           test_group["Purchase"])

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Sonuç: Test Stat = 2.6393, p-value = 0.1083 > 0.05

#Homojenlik varsayımı reddedilemez.

# Adım 2: Normallik Varsayımı ve VaryansHomojenliği sonuçlarına göre uygun testi seçiniz

#Varsayımlar sağlandığı için parametrik test kullanılır.

test_stat, pvalue = ttest_ind(control_group["Purchase"],
                              test_group["Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#Sonuç: Test Stat = -0.9416, p-value = 0.3493 >0.05 olduğu için ho reddedilemez

#Adım 3: Test sonucunda elde edilen p_valuedeğerini göz önünde bulundurarak kontrol ve test grubu satın alma ortalamaları arasında
# istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.


# Arada istatistiki olarak anlamlı bir fark yoktur.Çünkü p_value değeri 0.05 den büyüktür.

# Görev 4:  Sonuçların Analizi
#Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.

# YORUM : normallik ve homojenlik varsayımları reddedilemediği için parametrik testi kullandım. ( ttest_ind)

#Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz
# YORUM: En başta test ve kontrol gruplarının ortalamalarına baktığımızda aralarında bir fark görebilmiştik.
#Ancak hipotez testlerini yapıp incelediğimizde ortalama eşitliği hipotezini reddedemedik.Bu da bize ortalamalarda oluşan farkların tesadüfi olabileceğini gösteriyor.
#Bu yeni özelliğe geçmek bize anlamlı bir dönüşüm getirmeyebilir.