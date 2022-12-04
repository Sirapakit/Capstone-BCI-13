import mne
import mne.viz
import numpy as np
import json
from scipy import signal
from scipy.stats import mode
import os

path = '../json_convert_to_npy/chb24'
patient_chb = 'chb24'
json_filename_array = os.listdir(path)
json_filename_array.sort()

print('--------Start--------')
for index, json_filename in enumerate(json_filename_array):
    print(f'Investigating: {json_filename}')
    if json_filename.endswith('.json'):
        data = open('../' + 'json_convert_to_npy/' + patient_chb + '/' + json_filename)
        f = json.load(data)

        data_file = '../dataset/' + f['patient_ID'] + '/' + f['raw_name']
        raw = mne.io.read_raw(data_file)

        raw_array = raw.get_data()
        filter_band_1 = [-0.00746130275969432, -0.00775091228015498, -0.00803687583618559, -0.00831761219110410, -0.00859152635432147, -0.00885701632363083, -0.00911247994314634, -0.00935632184750005, -0.00958696046228121, -0.00980283503021094, -0.0100024126321907, -0.0101841951721465, -0.0103467262945138, -0.0104885982032757, -0.0106084583516705, -0.0107050159720369, -0.0107770484157523, -0.0108234072738497, -0.0108430242496626, -0.0108349167557493, -0.0107981932083777, -0.0107320579940071, -0.0106358160834862, -0.0105088772710783, -0.0103507600169348, -0.0101610948732458, -0.00993962747600702, -0.00968622108614084, -0.00940085866558823, -0.00908364447594568, -0.00873480518924006, -0.00835469050251206, -0.00794377325000289, -0.00750264900890155, -0.00703203519679987, -0.00653276966121191, -0.00600580876373075, -0.00545222496361186, -0.00487320390777551, -0.00427004103640315, -0.00364413771545254, -0.00299699690952590, -0.00233021841058220, -0.00164549363998214, -0.000944600043281034, -0.000229395099032949, 0.000498190035369813, 0.00123615721613286, 0.00198244831752100, 0.00273495252064312, 0.00349151385752632, 0.00424993898023541, 0.00500800512371454, 0.00576346823008322, 0.00651407120131354, 0.00725755224655404, 0.00799165328985059, 0.00871412840364894, 0.00942275223324948, 0.0101153283773230, 0.0107896976896881, 0.0114437464677946, 0.0120754144937552, 0.0126827028943150, 0.0132636817868430, 0.0138164976792747, 0.0143393805929141, 0.0148306508781302, 0.0152887256942328, 0.0157121251261990, 0.0160994779124213, 0.0164495267592713, 0.0167611332199954, 0.0170332821172886, 0.0172650854908090, 0.0174557860529000, 0.0176047601378619, 0.0177115201322593, 0.0177757163759463, 0.0177971385257398, 0.0177757163759463, 0.0177115201322593, 0.0176047601378619, 0.0174557860529000, 0.0172650854908090, 0.0170332821172886, 0.0167611332199954, 0.0164495267592713, 0.0160994779124213, 0.0157121251261990, 0.0152887256942328, 0.0148306508781302, 0.0143393805929141, 0.0138164976792747, 0.0132636817868430, 0.0126827028943150, 0.0120754144937552, 0.0114437464677946, 0.0107896976896881, 0.0101153283773230, 0.00942275223324948, 0.00871412840364894, 0.00799165328985059, 0.00725755224655404, 0.00651407120131354, 0.00576346823008322, 0.00500800512371454, 0.00424993898023541, 0.00349151385752632, 0.00273495252064312, 0.00198244831752100, 0.00123615721613286, 0.000498190035369813, -0.000229395099032949, -0.000944600043281034, -0.00164549363998214, -0.00233021841058220, -0.00299699690952590, -0.00364413771545254, -0.00427004103640315, -0.00487320390777551, -0.00545222496361186, -0.00600580876373075, -0.00653276966121191, -0.00703203519679987, -0.00750264900890155, -0.00794377325000289, -0.00835469050251206, -0.00873480518924006, -0.00908364447594568, -0.00940085866558823, -0.00968622108614084, -0.00993962747600702, -0.0101610948732458, -0.0103507600169348, -0.0105088772710783, -0.0106358160834862, -0.0107320579940071, -0.0107981932083777, -0.0108349167557493, -0.0108430242496626, -0.0108234072738497, -0.0107770484157523, -0.0107050159720369, -0.0106084583516705, -0.0104885982032757, -0.0103467262945138, -0.0101841951721465, -0.0100024126321907, -0.00980283503021094, -0.00958696046228121, -0.00935632184750005, -0.00911247994314634, -0.00885701632363083, -0.00859152635432147, -0.00831761219110410, -0.00803687583618559, -0.00775091228015498, -0.00746130275969432]
        filter_band_2 = [-0.00174052682807970, -0.00183618891780604, -0.00186796015439467, -0.00182873991969156, -0.00171284818676060, -0.00151620728379483, -0.00123649505714197, -0.000873265570839400, -0.000428034053484924, 9.56765469734395e-05, 0.000692329325551443, 0.00135440865877490, 0.00207249727553533, 0.00283539469140513, 0.00363027570668829, 0.00444288684793066, 0.00525777783867776, 0.00605856443394525, 0.00682821825953966, 0.00754937867649397, 0.00820468115570299, 0.00877709621010389, 0.00925027260145455, 0.00960887832396577, 0.00983893277365694, 0.00992812354396643, 0.00986610144612144, 0.00964474763589801, 0.00925840713309038, 0.00870408354028346, 0.00798159039510945, 0.00709365531463185, 0.00604597389941680, 0.00484721124403421, 0.00350894983448103, 0.00204558358440886, 0.000474158753230718, -0.00118583651824341, -0.00291273134369004, -0.00468297624822371, -0.00647148781033014, -0.00825202843815503, -0.00999761520215219, -0.0116809510204907, -0.0132748709826136, -0.0147527962107327, -0.0160891874073939, -0.0172599901256793, -0.0182430638306932, -0.0190185869976145, -0.0195694308110133, -0.0198814944878647, -0.0199439958356788, -0.0197497113678376, -0.0192951611186776, -0.0185807342170509, -0.0176107522731264, -0.0163934686915455, -0.0149410031259459, -0.0132692114156021, -0.0113974924742127, -0.00934853471323162, -0.00714800565729385, -0.00482418942752198, -0.00240757771102952, 6.95793157233808e-05, 0.00257375490177959, 0.00507065264950515, 0.00752573014759231, 0.00990473066297433, 0.0121742140576952, 0.0143020780638859, 0.0162580611730813, 0.0180142186734991, 0.0195453637961163, 0.0208294665001698, 0.0218480031312425, 0.0225862510080680, 0.0230335229230995, 0.0231833375602670, 0.0230335229230995, 0.0225862510080680, 0.0218480031312425, 0.0208294665001698, 0.0195453637961163, 0.0180142186734991, 0.0162580611730813, 0.0143020780638859, 0.0121742140576952, 0.00990473066297433, 0.00752573014759231, 0.00507065264950515, 0.00257375490177959, 6.95793157233808e-05, -0.00240757771102952, -0.00482418942752198, -0.00714800565729385, -0.00934853471323162, -0.0113974924742127, -0.0132692114156021, -0.0149410031259459, -0.0163934686915455, -0.0176107522731264, -0.0185807342170509, -0.0192951611186776, -0.0197497113678376, -0.0199439958356788, -0.0198814944878647, -0.0195694308110133, -0.0190185869976145, -0.0182430638306932, -0.0172599901256793, -0.0160891874073939, -0.0147527962107327, -0.0132748709826136, -0.0116809510204907, -0.00999761520215219, -0.00825202843815503, -0.00647148781033014, -0.00468297624822371, -0.00291273134369004, -0.00118583651824341, 0.000474158753230718, 0.00204558358440886, 0.00350894983448103, 0.00484721124403421, 0.00604597389941680, 0.00709365531463185, 0.00798159039510945, 0.00870408354028346, 0.00925840713309038, 0.00964474763589801, 0.00986610144612144, 0.00992812354396643, 0.00983893277365694, 0.00960887832396577, 0.00925027260145455, 0.00877709621010389, 0.00820468115570299, 0.00754937867649397, 0.00682821825953966, 0.00605856443394525, 0.00525777783867776, 0.00444288684793066, 0.00363027570668829, 0.00283539469140513, 0.00207249727553533, 0.00135440865877490, 0.000692329325551443, 9.56765469734395e-05, -0.000428034053484924, -0.000873265570839400, -0.00123649505714197, -0.00151620728379483, -0.00171284818676060, -0.00182873991969156, -0.00186796015439467, -0.00183618891780604, -0.00174052682807970]
        filter_band_3 = [-0.000935063880355104, -0.000716467958274841, -0.000367310774766668, 0.000107356912361869, 0.000694114246599031, 0.00137140377823110, 0.00211020685124590, 0.00287514401913025, 0.00362596216505807, 0.00431934975120557, 0.00491100358629276, 0.00535785559269879, 0.00562035706193762, 0.00566471143240761, 0.00546494513137347, 0.00500470969811578, 0.00427871721571191, 0.00329372475462800, 0.00206900157021214, 0.000636234482810177, -0.000961148697070902, -0.00266923170384880, -0.00442540563817067, -0.00616064937821346, -0.00780221172279560, -0.00927659125369148, -0.0105126927959460, -0.0114450271722306, -0.0120168143690486, -0.0121828497014928, -0.0119119982610554, -0.0111891947651609, -0.0100168435293784, -0.00841553602062347, -0.00642403044718667, -0.00409846801653467, -0.00151083259825130, 0.00125330679071151, 0.00409769941981959, 0.00691886134021195, 0.00960994206240403, 0.0120648612991016, 0.0141825522219676, 0.0158711388410219, 0.0170518733874205, 0.0176626651854870, 0.0176610453466990, 0.0170264313021942, 0.0157615810059490, 0.0138931576079612, 0.0114713602987942, 0.00856861445931450, 0.00527735267808548, 0.00170695602354850, -0.00202003941934131, -0.00577233384574431, -0.00941468918703733, -0.0128130045956715, -0.0158394446283015, -0.0183774175027099, -0.0203262037396750, -0.0216050466480413, -0.0221565351069671, -0.0219491352480702, -0.0209787599399541, -0.0192693021595746, -0.0168720989147923, -0.0138643347213228, -0.0103464360094567, -0.00643854850098496, -0.00227622687271384, 0.00199450164276388, 0.00622251203293075, 0.0102571883388552, 0.0139540457998628, 0.0171801498075798, 0.0198191201944185, 0.0217755249377974, 0.0229784908407991, 0.0233843892174715, 0.0229784908407991, 0.0217755249377974, 0.0198191201944185, 0.0171801498075798, 0.0139540457998628, 0.0102571883388552, 0.00622251203293075, 0.00199450164276388, -0.00227622687271384, -0.00643854850098496, -0.0103464360094567, -0.0138643347213228, -0.0168720989147923, -0.0192693021595746, -0.0209787599399541, -0.0219491352480702, -0.0221565351069671, -0.0216050466480413, -0.0203262037396750, -0.0183774175027099, -0.0158394446283015, -0.0128130045956715, -0.00941468918703733, -0.00577233384574431, -0.00202003941934131, 0.00170695602354850, 0.00527735267808548, 0.00856861445931450, 0.0114713602987942, 0.0138931576079612, 0.0157615810059490, 0.0170264313021942, 0.0176610453466990, 0.0176626651854870, 0.0170518733874205, 0.0158711388410219, 0.0141825522219676, 0.0120648612991016, 0.00960994206240403, 0.00691886134021195, 0.00409769941981959, 0.00125330679071151, -0.00151083259825130, -0.00409846801653467, -0.00642403044718667, -0.00841553602062347, -0.0100168435293784, -0.0111891947651609, -0.0119119982610554, -0.0121828497014928, -0.0120168143690486, -0.0114450271722306, -0.0105126927959460, -0.00927659125369148, -0.00780221172279560, -0.00616064937821346, -0.00442540563817067, -0.00266923170384880, -0.000961148697070902, 0.000636234482810177, 0.00206900157021214, 0.00329372475462800, 0.00427871721571191, 0.00500470969811578, 0.00546494513137347, 0.00566471143240761, 0.00562035706193762, 0.00535785559269879, 0.00491100358629276, 0.00431934975120557, 0.00362596216505807, 0.00287514401913025, 0.00211020685124590, 0.00137140377823110, 0.000694114246599031, 0.000107356912361869, -0.000367310774766668, -0.000716467958274841, -0.000935063880355104]
        filter_band_4 = [-0.000115262676354512, 0.000414330876085213, 0.00107029561950722, 0.00179727218287726, 0.00252452307216603, 0.00317191062723746, 0.00365721726101749, 0.00390419235232974, 0.00385061463827836, 0.00345562312737219, 0.00270559872949103, 0.00161797280623633, 0.000242491906654552, -0.00134033099296464, -0.00302361493940997, -0.00468114828389334, -0.00617661398991259, -0.00737434011093271, -0.00815074756647958, -0.00840556520762389, -0.00807185400370896, -0.00712393328680929, -0.00558243120447373, -0.00351588115534616, -0.00103854220607017, 0.00169558465726092, 0.00450226382660877, 0.00717947635406298, 0.00952197128055182, 0.0113368660453038, 0.0124591141952280, 0.0127656173249562, 0.0121868129328093, 0.0107147196695126, 0.00840665762081433, 0.00538416795793750, 0.00182701155514502, -0.00203749646938852, -0.00594918890225197, -0.00963282369449316, -0.0128177040933502, -0.0152577253338188, -0.0167503509848913, -0.0171530541780348, -0.0163959044888077, -0.0144892320632713, -0.0115256401592229, -0.00767604180166702, -0.00317983633339256, 0.00167021554969268, 0.00654744792607948, 0.0111137579932830, 0.0150435102145133, 0.0180471550529134, 0.0198928223045741, 0.0204242602796739, 0.0195737274797716, 0.0173687875691551, 0.0139323873964806, 0.00947608081092836, 0.00428676266803078, -0.00129223958827422, -0.00688444150983242, -0.0121062291986226, -0.0165937982506089, -0.0200290710114888, -0.0221627080162171, -0.0228325179081131, -0.0219758855689684, -0.0196352585255532, -0.0159562267490835, -0.0111782646931419, -0.00561873759681809, 0.000348732764821034, 0.00632003133075172, 0.0118886221248580, 0.0166739329572456, 0.0203480238672081, 0.0226586269800029, 0.0234469017077285, 0.0226586269800029, 0.0203480238672081, 0.0166739329572456, 0.0118886221248580, 0.00632003133075172, 0.000348732764821034, -0.00561873759681809, -0.0111782646931419, -0.0159562267490835, -0.0196352585255532, -0.0219758855689684, -0.0228325179081131, -0.0221627080162171, -0.0200290710114888, -0.0165937982506089, -0.0121062291986226, -0.00688444150983242, -0.00129223958827422, 0.00428676266803078, 0.00947608081092836, 0.0139323873964806, 0.0173687875691551, 0.0195737274797716, 0.0204242602796739, 0.0198928223045741, 0.0180471550529134, 0.0150435102145133, 0.0111137579932830, 0.00654744792607948, 0.00167021554969268, -0.00317983633339256, -0.00767604180166702, -0.0115256401592229, -0.0144892320632713, -0.0163959044888077, -0.0171530541780348, -0.0167503509848913, -0.0152577253338188, -0.0128177040933502, -0.00963282369449316, -0.00594918890225197, -0.00203749646938852, 0.00182701155514502, 0.00538416795793750, 0.00840665762081433, 0.0107147196695126, 0.0121868129328093, 0.0127656173249562, 0.0124591141952280, 0.0113368660453038, 0.00952197128055182, 0.00717947635406298, 0.00450226382660877, 0.00169558465726092, -0.00103854220607017, -0.00351588115534616, -0.00558243120447373, -0.00712393328680929, -0.00807185400370896, -0.00840556520762389, -0.00815074756647958, -0.00737434011093271, -0.00617661398991259, -0.00468114828389334, -0.00302361493940997, -0.00134033099296464, 0.000242491906654552, 0.00161797280623633, 0.00270559872949103, 0.00345562312737219, 0.00385061463827836, 0.00390419235232974, 0.00365721726101749, 0.00317191062723746, 0.00252452307216603, 0.00179727218287726, 0.00107029561950722, 0.000414330876085213, -0.000115262676354512]
        filter_band_5 = [0.000682399660233684, 0.00138656908759435, 0.00208789570459458, 0.00265696461458574, 0.00296563041658014, 0.00290821399663400, 0.00242115016640657, 0.00149800830990320, 0.000197293350403221, -0.00135868321165896, -0.00299439803592753, -0.00450039618262016, -0.00565919504739980, -0.00627468249207828, -0.00620118377307079, -0.00536816209226318, -0.00379684743795580, -0.00160594082323894, 0.000995172085252156, 0.00372569303863716, 0.00626350432254239, 0.00828288561283195, 0.00949546063794010, 0.00968929323731183, 0.00876099109919219, 0.00673627780248919, 0.00377571360125400, 0.000163954464601474, -0.00371705967606194, -0.00742854557818289, -0.0105246632667242, -0.0126059776145371, -0.0133701846121521, -0.0126537221594912, -0.0104587132814382, -0.00696124456731494, -0.00249909924583446, 0.00246049896115471, 0.00737010853071887, 0.0116630446615584, 0.0148192540547233, 0.0164283780412832, 0.0162423409269026, 0.0142107830240861, 0.0104944847916217, 0.00545440389049334, -0.000383210404898814, -0.00638228537715145, -0.0118670745979614, -0.0161991607219319, -0.0188524390514430, -0.0194771988416061, -0.0179454695091347, -0.0143718102397071, -0.00910647574082454, -0.00270107535011527, 0.00414991390601874, 0.0106855035176741, 0.0161639077477362, 0.0199478317023608, 0.0215794070144622, 0.0208358753874112, 0.0177592134832815, 0.0126558220797884, 0.00606583424091618, -0.00129486707721528, -0.00861360842426269, -0.0150720227791720, -0.0199389224503000, -0.0226542592445895, -0.0228944024345445, -0.0206110350570209, -0.0160389571478205, -0.00967164739347422, -0.00220715851319816, 0.00552962929888155, 0.0126796044112207, 0.0184463175834362, 0.0221860822319712, 0.0234809375152661, 0.0221860822319712, 0.0184463175834362, 0.0126796044112207, 0.00552962929888155, -0.00220715851319816, -0.00967164739347422, -0.0160389571478205, -0.0206110350570209, -0.0228944024345445, -0.0226542592445895, -0.0199389224503000, -0.0150720227791720, -0.00861360842426269, -0.00129486707721528, 0.00606583424091618, 0.0126558220797884, 0.0177592134832815, 0.0208358753874112, 0.0215794070144622, 0.0199478317023608, 0.0161639077477362, 0.0106855035176741, 0.00414991390601874, -0.00270107535011527, -0.00910647574082454, -0.0143718102397071, -0.0179454695091347, -0.0194771988416061, -0.0188524390514430, -0.0161991607219319, -0.0118670745979614, -0.00638228537715145, -0.000383210404898814, 0.00545440389049334, 0.0104944847916217, 0.0142107830240861, 0.0162423409269026, 0.0164283780412832, 0.0148192540547233, 0.0116630446615584, 0.00737010853071887, 0.00246049896115471, -0.00249909924583446, -0.00696124456731494, -0.0104587132814382, -0.0126537221594912, -0.0133701846121521, -0.0126059776145371, -0.0105246632667242, -0.00742854557818289, -0.00371705967606194, 0.000163954464601474, 0.00377571360125400, 0.00673627780248919, 0.00876099109919219, 0.00968929323731183, 0.00949546063794010, 0.00828288561283195, 0.00626350432254239, 0.00372569303863716, 0.000995172085252156, -0.00160594082323894, -0.00379684743795580, -0.00536816209226318, -0.00620118377307079, -0.00627468249207828, -0.00565919504739980, -0.00450039618262016, -0.00299439803592753, -0.00135868321165896, 0.000197293350403221, 0.00149800830990320, 0.00242115016640657, 0.00290821399663400, 0.00296563041658014, 0.00265696461458574, 0.00208789570459458, 0.00138656908759435, 0.000682399660233684]
        filter_band_6 = [0.00132880175369376, 0.00197324918065014, 0.00237008427336357, 0.00235292793334883, 0.00182359683244801, 0.000785198089478375, -0.000643819958049911, -0.00223952308845124, -0.00370640197940848, -0.00473042445109492, -0.00504191950290612, -0.00447619242283914, -0.00301924834807534, -0.000827995370668348, 0.00178143356477442, 0.00437776372513758, 0.00648523921709865, 0.00766938349988061, 0.00762257934713234, 0.00623308485081286, 0.00362307704852510, 0.000146174995460478, -0.00365811585888389, -0.00714767849277411, -0.00968601623470309, -0.0107572138881706, -0.0100670029385113, -0.00761059233170722, -0.00369285591628089, 0.00110567962126833, 0.00601412275664081, 0.0101954089570125, 0.0128893369171106, 0.0135499500738959, 0.0119525316920171, 0.00824969137878354, 0.00296411063203890, -0.00308380354282560, -0.00890364420213361, -0.0134981729440442, -0.0160348896159029, -0.0159963638611894, -0.0132822330150702, -0.00824319463045547, -0.00163848493384041, 0.00547860765027439, 0.0119299336250842, 0.0166090051287531, 0.0186718244625875, 0.0176889300429223, 0.0137312759991155, 0.00737320044054926, -0.000390412642878154, -0.00830094374938396, -0.0150419233067909, -0.0194600138248364, -0.0207636855918955, -0.0186651391953733, -0.0134399938109430, -0.00589280866656675, 0.00276761593911118, 0.0111237026500028, 0.0177834172430625, 0.0216143408799702, 0.0219377813303763, 0.0186493963512144, 0.0122448208267298, 0.00374465544305351, -0.00546978638567280, -0.0138832754054602, -0.0200983905061679, -0.0230699350837493, -0.0222823468159586, -0.0178397216938012, -0.0104526381334016, -0.00132332565798365, 0.00805207262185972, 0.0161312823870934, 0.0215822679989937, 0.0235051412750471, 0.0215822679989937, 0.0161312823870934, 0.00805207262185972, -0.00132332565798365, -0.0104526381334016, -0.0178397216938012, -0.0222823468159586, -0.0230699350837493, -0.0200983905061679, -0.0138832754054602, -0.00546978638567280, 0.00374465544305351, 0.0122448208267298, 0.0186493963512144, 0.0219377813303763, 0.0216143408799702, 0.0177834172430625, 0.0111237026500028, 0.00276761593911118, -0.00589280866656675, -0.0134399938109430, -0.0186651391953733, -0.0207636855918955, -0.0194600138248364, -0.0150419233067909, -0.00830094374938396, -0.000390412642878154, 0.00737320044054926, 0.0137312759991155, 0.0176889300429223, 0.0186718244625875, 0.0166090051287531, 0.0119299336250842, 0.00547860765027439, -0.00163848493384041, -0.00824319463045547, -0.0132822330150702, -0.0159963638611894, -0.0160348896159029, -0.0134981729440442, -0.00890364420213361, -0.00308380354282560, 0.00296411063203890, 0.00824969137878354, 0.0119525316920171, 0.0135499500738959, 0.0128893369171106, 0.0101954089570125, 0.00601412275664081, 0.00110567962126833, -0.00369285591628089, -0.00761059233170722, -0.0100670029385113, -0.0107572138881706, -0.00968601623470309, -0.00714767849277411, -0.00365811585888389, 0.000146174995460478, 0.00362307704852510, 0.00623308485081286, 0.00762257934713234, 0.00766938349988061, 0.00648523921709865, 0.00437776372513758, 0.00178143356477442, -0.000827995370668348, -0.00301924834807534, -0.00447619242283914, -0.00504191950290612, -0.00473042445109492, -0.00370640197940848, -0.00223952308845124, -0.000643819958049911, 0.000785198089478375, 0.00182359683244801, 0.00235292793334883, 0.00237008427336357, 0.00197324918065014, 0.00132880175369376]
        filter_band_7 = [0.00170803490229575, 0.00203159257727944, 0.00183373160602912, 0.00102965017130619, -0.000288332424937886, -0.00184950385530197, -0.00325778546872152, -0.00408939719098231, -0.00401159860863592, -0.00289062631205755, -0.000856952493878816, 0.00169507424654060, 0.00418009089950548, 0.00595468008709178, 0.00648051960851538, 0.00547696876991433, 0.00302156150418032, -0.000432892716684140, -0.00413658388639172, -0.00720438904958414, -0.00882638967193634, -0.00847733702409265, -0.00607166940505447, -0.00202064166820212, 0.00283013130240197, 0.00737570469168288, 0.0105035952397161, 0.0113649328023677, 0.00959907272085606, 0.00545325681841027, -0.000238596071500596, -0.00622119039210128, -0.0110951640221533, -0.0136450583914171, -0.0131409183143205, -0.00953894350134712, -0.00352746409452231, 0.00360050532493433, 0.0102257019912696, 0.0147720397931800, 0.0160823834253325, 0.0137108678058944, 0.00805830828117956, 0.000311985419064216, -0.00780350209536374, -0.0144121306229670, -0.0179223102466770, -0.0174109462538179, -0.0128628317989708, -0.00520389846831090, 0.00388607589662410, 0.0123437651311030, 0.0181935487029687, 0.0200114330087317, 0.0172721444223132, 0.0104946618605282, 0.00114693982683470, -0.00867355032638994, -0.0167136063662731, -0.0210846753485359, -0.0207088746402777, -0.0155847679268937, -0.00680734006952815, 0.00366687435377616, 0.0134589406284540, 0.0203116977711379, 0.0226136050256544, 0.0197798838999544, 0.0124003229886479, 0.00211651994531225, -0.00874590504849879, -0.0177071332601826, -0.0227034219207163, -0.0225657482830972, -0.0172950508045330, -0.00806887599538339, 0.00302365144827168, 0.0134584431084348, 0.0208551044585293, 0.0235240031480327, 0.0208551044585293, 0.0134584431084348, 0.00302365144827168, -0.00806887599538339, -0.0172950508045330, -0.0225657482830972, -0.0227034219207163, -0.0177071332601826, -0.00874590504849879, 0.00211651994531225, 0.0124003229886479, 0.0197798838999544, 0.0226136050256544, 0.0203116977711379, 0.0134589406284540, 0.00366687435377616, -0.00680734006952815, -0.0155847679268937, -0.0207088746402777, -0.0210846753485359, -0.0167136063662731, -0.00867355032638994, 0.00114693982683470, 0.0104946618605282, 0.0172721444223132, 0.0200114330087317, 0.0181935487029687, 0.0123437651311030, 0.00388607589662410, -0.00520389846831090, -0.0128628317989708, -0.0174109462538179, -0.0179223102466770, -0.0144121306229670, -0.00780350209536374, 0.000311985419064216, 0.00805830828117956, 0.0137108678058944, 0.0160823834253325, 0.0147720397931800, 0.0102257019912696, 0.00360050532493433, -0.00352746409452231, -0.00953894350134712, -0.0131409183143205, -0.0136450583914171, -0.0110951640221533, -0.00622119039210128, -0.000238596071500596, 0.00545325681841027, 0.00959907272085606, 0.0113649328023677, 0.0105035952397161, 0.00737570469168288, 0.00283013130240197, -0.00202064166820212, -0.00607166940505447, -0.00847733702409265, -0.00882638967193634, -0.00720438904958414, -0.00413658388639172, -0.000432892716684140, 0.00302156150418032, 0.00547696876991433, 0.00648051960851538, 0.00595468008709178, 0.00418009089950548, 0.00169507424654060, -0.000856952493878816, -0.00289062631205755, -0.00401159860863592, -0.00408939719098231, -0.00325778546872152, -0.00184950385530197, -0.000288332424937886, 0.00102965017130619, 0.00183373160602912, 0.00203159257727944, 0.00170803490229575]
        filter_band_8 = [0.00175136343908006, 0.00155226033518152, 0.000668404486553345, -0.000739434336048251, -0.00225692419357041, -0.00333501881701138, -0.00348046547651369, -0.00245372537465612, -0.000400130098721296, 0.00214315914117983, 0.00438229135072609, 0.00551198770287292, 0.00499584270882180, 0.00278626601856835, -0.000599702577623739, -0.00419030799050297, -0.00683585790166384, -0.00757425419863861, -0.00596971704165011, -0.00230805675605025, 0.00242969581525211, 0.00682557047779254, 0.00944850686901667, 0.00931724524536599, 0.00625326617184259, 0.00100009742764349, -0.00494682171755107, -0.00976476682196353, -0.0118626822588745, -0.0104029423302331, -0.00561571468570452, 0.00120765945020331, 0.00805921709120811, 0.0128062899294471, 0.0138560127481125, 0.0106851291985834, 0.00406002869281167, -0.00413826002240539, -0.0114480822411657, -0.0155686565203796, -0.0150850006129407, -0.00994760237991845, -0.00154576596648321, 0.00766512034581670, 0.0148834694103295, 0.0178167972956611, 0.0154103693209691, 0.00821737074625264, -0.00171712736267325, -0.0114385108867155, -0.0179652214100213, -0.0192068063815739, -0.0146336583282255, -0.00548375924038437, 0.00557030872851583, 0.0152052938496057, 0.0204512205724119, 0.0196106073024864, 0.0128073344877175, 0.00198774901977106, -0.00963785496713856, -0.0185526193689546, -0.0220024029967929, -0.0188502368968888, -0.00994978846884724, 0.00208453927564939, 0.0136494261403938, 0.0212373577196148, 0.0225059732098837, 0.0170043627367659, 0.00633014693217177, -0.00633660407684108, -0.0171859990420399, -0.0229305664729076, -0.0218067451863520, -0.0141189323306791, -0.00215746485840819, 0.0104875222015027, 0.0200096643361083, 0.0235385213276456, 0.0200096643361083, 0.0104875222015027, -0.00215746485840819, -0.0141189323306791, -0.0218067451863520, -0.0229305664729076, -0.0171859990420399, -0.00633660407684108, 0.00633014693217177, 0.0170043627367659, 0.0225059732098837, 0.0212373577196148, 0.0136494261403938, 0.00208453927564939, -0.00994978846884724, -0.0188502368968888, -0.0220024029967929, -0.0185526193689546, -0.00963785496713856, 0.00198774901977106, 0.0128073344877175, 0.0196106073024864, 0.0204512205724119, 0.0152052938496057, 0.00557030872851583, -0.00548375924038437, -0.0146336583282255, -0.0192068063815739, -0.0179652214100213, -0.0114385108867155, -0.00171712736267325, 0.00821737074625264, 0.0154103693209691, 0.0178167972956611, 0.0148834694103295, 0.00766512034581670, -0.00154576596648321, -0.00994760237991845, -0.0150850006129407, -0.0155686565203796, -0.0114480822411657, -0.00413826002240539, 0.00406002869281167, 0.0106851291985834, 0.0138560127481125, 0.0128062899294471, 0.00805921709120811, 0.00120765945020331, -0.00561571468570452, -0.0104029423302331, -0.0118626822588745, -0.00976476682196353, -0.00494682171755107, 0.00100009742764349, 0.00625326617184259, 0.00931724524536599, 0.00944850686901667, 0.00682557047779254, 0.00242969581525211, -0.00230805675605025, -0.00596971704165011, -0.00757425419863861, -0.00683585790166384, -0.00419030799050297, -0.000599702577623739, 0.00278626601856835, 0.00499584270882180, 0.00551198770287292, 0.00438229135072609, 0.00214315914117983, -0.000400130098721296, -0.00245372537465612, -0.00348046547651369, -0.00333501881701138, -0.00225692419357041, -0.000739434336048251, 0.000668404486553345, 0.00155226033518152, 0.00175136343908006]

        array_length = raw_array.shape[1]
        seizure_event = { 'inter_ictal' : 0, 'seizure_onset' : 1, 'ictal' : 2 }
        event_array = np.zeros((1,array_length))

        sampling_rate = 256
        soz_start_sample = sampling_rate * (f['time_stamp']['start'][0] - 30)
        start_sample = sampling_rate * (f['time_stamp']['start'][0])
        end_sample = sampling_rate * (f['time_stamp']['end'][0])

        def box_text(text):
            lines = text.splitlines()
            width = max(len(s) for s in lines)
            res = [' '*7 + '#' + '─' * width + '#']
            for s in lines:
                res.append(' '*7 + '│' + (s + ' ' * width)[:width] + '│')
            res.append(' '*7 + '#' + '─' * width + '#')
            return '\n'.join(res)

        number_of_seizure = f['number_of_seizure']
        if (number_of_seizure == 0 ):
            print(box_text('NO SEIZURE DETECT'))
            np.append(raw_array, event_array, axis=0)

        elif (number_of_seizure == 1):
            print(box_text(f'{str(number_of_seizure).upper()} SEIZURE DETECT'))
            event_array[0][soz_start_sample:start_sample] = seizure_event['seizure_onset']
            event_array[0][start_sample:end_sample] = seizure_event['ictal']
            np.append(raw_array, event_array, axis=0)

        elif (number_of_seizure >= 2):
            print(box_text(f'{str(number_of_seizure).upper()} SEIZURE DETECT'))
            for i in range (number_of_seizure):
                event_array[0][sampling_rate * (f['time_stamp']['start'][i] - 30):
                            sampling_rate * (f['time_stamp']['start'][i])] = seizure_event['seizure_onset']
                event_array[0][sampling_rate * (f['time_stamp']['start'][i]):
                                sampling_rate * (f['time_stamp']['end'][i])] = seizure_event['ictal']
                np.append(raw_array, event_array, axis=0)

        else:
            print(box_text('ERROR: WRONG NUMBER_SEIZURE'))

        channels_number = f['channels']["number"]
        new_channels_number = channels_number + 1
        raw_array_with_seizure_event = np.zeros((new_channels_number, array_length))

        raw_array_with_seizure_event[:channels_number][:] = raw_array
        raw_array_with_seizure_event[channels_number][:] = event_array

        Fp2_T8 = (f['channels']['Fp2_F8']) - 1
        F8_T8 = (f['channels']['F8_T8']) - 1
        Fp2_T8_channel = raw_array_with_seizure_event[Fp2_T8] 
        F8_T8_channel = raw_array_with_seizure_event[F8_T8]
        seizure_event_channel = raw_array_with_seizure_event[channels_number]

        data_array = np.zeros((17, array_length))
        data_array[0][:] = signal.filtfilt(filter_band_1, 1, Fp2_T8_channel)
        data_array[1][:] = signal.filtfilt(filter_band_2, 1, Fp2_T8_channel)
        data_array[2][:] = signal.filtfilt(filter_band_3, 1, Fp2_T8_channel)
        data_array[3][:] = signal.filtfilt(filter_band_4, 1, Fp2_T8_channel)
        data_array[4][:] = signal.filtfilt(filter_band_5, 1, Fp2_T8_channel)
        data_array[5][:] = signal.filtfilt(filter_band_6, 1, Fp2_T8_channel)
        data_array[6][:] = signal.filtfilt(filter_band_7, 1, Fp2_T8_channel)
        data_array[7][:] = signal.filtfilt(filter_band_8, 1, Fp2_T8_channel)

        data_array[8][:] = signal.filtfilt(filter_band_1, 1, F8_T8_channel)
        data_array[9][:] = signal.filtfilt(filter_band_2, 1, F8_T8_channel)
        data_array[10][:] = signal.filtfilt(filter_band_3, 1, F8_T8_channel)
        data_array[11][:] = signal.filtfilt(filter_band_4, 1, F8_T8_channel)
        data_array[12][:] = signal.filtfilt(filter_band_5, 1, F8_T8_channel)
        data_array[13][:] = signal.filtfilt(filter_band_6, 1, F8_T8_channel)
        data_array[14][:] = signal.filtfilt(filter_band_7, 1, F8_T8_channel)
        data_array[15][:] = signal.filtfilt(filter_band_8, 1, F8_T8_channel)

        data_array[16][:] = seizure_event_channel 
        
        band, chn = 8, 2 
        energy_array = np.zeros((17, int(array_length/(sampling_rate*2))))
        for feat in range(band * chn + 1): 
            start, end = 0, 512
            count = 0
            if (feat != band * chn):
                while (end <= array_length):
                    new_sub_array = np.zeros((1, 512))
                    new_sub_array = data_array[feat][:][start: end]
                    energy_one_band = np.sum(np.power(new_sub_array, 2))
                    energy_array[feat][count] = energy_one_band
                    start, end = end, end + 512
                    count += 1
            else : 
                while (end <= array_length):
                    energy_array[feat][count] = mode(data_array[feat][:][start: end], axis=None)[0][0] 
                    start, end = end, end + 512
                    count += 1
        
        for i in range(16):
            energy_array[i] = (energy_array[i]-np.min(energy_array[i]))/(np.max(energy_array[i])-np.min(energy_array[i]))


        data = energy_array
        save_path = './energy_bands/' + patient_chb
        filename = 'data_' + f['raw_name'].split('.')[0] + '_energy'
        np.save(os.path.join( save_path, filename ), data)

    else:
        print(f'-------------  {json_filename} is not an edf file  -------------')
        continue

print('--------Stop--------')
