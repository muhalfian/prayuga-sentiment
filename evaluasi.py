import needed.db_mysql as db_mysql
import helper.preprocessing as preprocessing
import analyzer.impress as impress;
import analyzer.naiveBayes as naiveBayes;
import json;

naiveBayes.initial();

sql = "SELECT * FROM eval_opinion";
db_mysql.executeSql(sql);
result = db_mysql.fetch('all');
for x in result:
    opini = x[1];
    k = preprocessing.do(opini);
    print k;

    v = impress.play(k,'eval');
    vNaive = naiveBayes.play(k);

    arr_word    = '';
    arr_counted = '';
    arr_score   = '';
    i = 0;
    for word in v['words']:
        if(i == 0):
            arr_word    = arr_word + word['word']+"|"+str(word['type'])+"|"+str(word['value']);
            arr_counted = arr_counted + v['counted'][i];
            arr_score   = arr_score + str(v['score'][i]);
        else:
            arr_word = arr_word+";"+word['word']+"|"+str(word['type'])+"|"+str(word['value']);
            arr_counted = arr_counted +";"+ v['counted'][i];
            arr_score   = arr_score +";"+ str(v['score'][i]);
        i = i+1;

    roleGroup = str(json.dumps(v['roleGroup']));
    # if(v == 'positif'):
    # 	v = 1;
    # elif(v=='negatif'):
    # 	v = -1;
    # else:
    # 	v = 0;
    sql = '''UPDATE eval_opinion SET hasil=%d, arr_word="%s", arr_score="%s", arr_counted="%s", role_group='%s', hasil_naive_bayes=%d WHERE id=%d''' % (v['sentiment'],arr_word,arr_score,arr_counted,roleGroup,vNaive,x[0]);
    db_mysql.executeSql(sql);
    db_mysql.commit();
    print str(v['sentiment'])+" :: "+opini;
    print "====================================";