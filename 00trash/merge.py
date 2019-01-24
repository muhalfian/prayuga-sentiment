import db_mysql

sql = ''' SELECT * FROM sentimental_word ''';
db_mysql.executeSql(sql);
words = db_mysql.fetch('all');

i=0;

for word in words:
    idword = word[0];
    typeword = word[2];
    valword = word[3];
    word = word[1];
    sql = ''' SELECT * FROM main_dict WHERE word="%s" ''' % (word);
    db_mysql.executeSql(sql);
    main_dict = db_mysql.fetch('one');
    if (main_dict != None):
    	if (main_dict[0] > 2004):
	    	i = i +1;
	    	print i;
	    	print word + " " +str(idword)+" "+str(typeword)+" "+str(valword);
	    	print main_dict[1] + " " +str(main_dict[0])+" "+str(main_dict[2])+" "+str(main_dict[3]);
	        sql = ''' UPDATE main_dict SET type="%s", value=%d WHERE id=%d ''' % (typeword.lower(),valword,main_dict[0]);
	        print sql;
	        db_mysql.executeSql(sql);
    else:
    	sql = ''' INSERT INTO main_dict (word, type, value) VALUES ("%s","%s",%d) ''' % (word,typeword.lower(),valword);
        print "ga ada"+sql;
        db_mysql.executeSql(sql);
#     if (valword != None and typeword != None):
#         sql = ''' UPDATE mining_dict_en SET type="%s", value=%d WHERE id=%d ''' % (typeword,valword,idword);
#         print sql;
#         db_mysql.executeSql(sql);
#     elif (typeword != None):
#         sql = ''' UPDATE mining_dict_en SET type="%s" WHERE id=%d ''' % (typeword,idword);
#         print sql;
#         db_mysql.executeSql(sql);
#     elif (valword != None):
#         sql = ''' UPDATE mining_dict_en SET value=%d WHERE id=%d ''' % (valword,idword);
#         print sql;
#         db_mysql.executeSql(sql);
db_mysql.commit();