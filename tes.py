#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import needed.db_mysql as db_mysql
import helper.preprocessing as preprocessing
import analyzer.impress as impress

# q = '"@jokowi"';
# since = '2017-01-09';
# until = '2017-08-01';
# twitter.play(q,since,until);

kalimat = "Kalau sampai permohonan tsb. dikabulkan MA. negera/pemerintah akan digoyang trus oleh mereka sampai keinginan syahwatnya tersalurkan seperti pada pilkada DKI 2017 behasil dan sukses dengan bantuan logo islam. Target berikutnya adalah pilpres 2019 mereka akan mainkan pertama PION SARA. kedua PION kesenjangan sosial. ketiga PION HAM. dan terakhir pion adu domba. Jika hal tsb tdk diantisipasi oleh pemerintah dan jajarannya maka hilanglah kepercayaan rakyat. yg terjadi kemudian adalah.pemodal dan para konglomerat pindah ke LN. yg warga negara asli indonesia tidak ada pilihan ngungsi ke gunung. Penegak HUKUM harus perpihak kepada kepentingan bangsa dan negara secara keseluruhan. Kalau ini dikabulkan MK apa yg terjadi adalah NKRI pasti secara perlahan lahan àkan PECAH. Yang ingin negara hilafah. yg ingin neg. islam. yg nasrani. yg. budha. yg. hindu. yg. kepercayaan juga mendirikan negaranya sendiri. Pemerintah harus WASPADA. Kpd. Bpk. JOKOWI Presiden RI rakyat bersama anda berjuang dibelakangMu. Semoga Alloh SWT memberikan kesehatan dan kekuatan bathin melawan manusia2 serakah yg tdk pernah puas. Yaaa Alloh berikanlah kekuatan kpd Bpk. Presiden untuk melindungi rakyatnya dari kehancuran. Yaaa Alloh engkau Maha Mengetahui tunjukkanlah bahwa yg bathil adalah bathil. yg baik tunjukkanlah baik. Hanya KepadaMu yaaa Alloh tempat memohon dan mengadu. kabulkan doa kami. semoga Bp. Jokowi dalam perlindunganNya. Amiin YRA.";
keyword = preprocessing.do(kalimat);
hasil   = impress.play(keyword,11);

print "Kalimat      : \n"+kalimat;
print "Preprocessing: ";
print len(keyword);
print keyword;
print "Klasifikasi kata: ";
print len(hasil['counted']);
print hasil['counted'];
print hasil['score'];
print "Hasil Sentimen : "+str(hasil['sentiment']);

i = 0;
j = 0;
for x in hasil['counted']:
	if(x == 'lxx'):
		print keyword[i];
		print hasil['roleGroup'][j];
		j = j + 1;
	i = i + 1;

