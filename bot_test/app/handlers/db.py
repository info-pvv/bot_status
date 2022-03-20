import sqlite3

def get_users(user_id):
    conn = sqlite3.connect('health.db', check_same_thread=False)
    user = conn.execute(f'SELECT * FROM Users WHERE user_id ={user_id}').fetchone()
    conn.close()
    if user is None:
        return None
    else:
        user_1 = user[1]
        return user_1

def get_user_status_admin(user_id):
    conn = sqlite3.connect('health.db', check_same_thread=False)
    user = conn.execute(f'''select users.user_id
                            from users
                                left join id_status on id_status.user_id=users.user_id
                            where id_status.enable_admin and users.user_id={user_id}''').fetchone()
    conn.close()
    if user is None:
        return False
    else:
        return True

def insert_users(user_id:int,user_first_name:str,user_last_name:str,username:str):
    conn = sqlite3.connect('health.db', check_same_thread=False)
    conn.execute(f'''INSERT INTO Users (user_id,first_name,last_name,username) VALUES ({user_id},'{user_first_name}','{user_last_name}','{username}')''')
    conn.commit()
    conn.close()
    return

def insert_FIO(user_id:int,user_first_name:str,user_last_name:str,username:str):
    conn = sqlite3.connect('health.db', check_same_thread=False)
    conn.execute(f'''INSERT INTO FIO (user_id,first_name,last_name,patronymic_name) VALUES ({user_id},'{user_first_name}','{user_last_name}','{username}')''')
    conn.commit()
    conn.close()
    return

def update_users(user_id:int,user_first_name:str,user_last_name:str,username:str):
    conn = sqlite3.connect('health.db', check_same_thread=False)
    conn.execute(f'''UPDATE Users SET first_name='{user_first_name}',last_name='{user_last_name}',username='{username}' WHERE user_id={user_id}''')
    conn.commit()
    conn.close()
    return

def get_health(user_id):
    conn = sqlite3.connect('health.db', check_same_thread=False)
    user = conn.execute(f'SELECT * FROM health WHERE id ={user_id}').fetchone()
    conn.close()
    if user is None:
        return None
    else:
        user_1 = user[1]
        return user_1

def insert_health(user_id:int,status:str):
    conn = sqlite3.connect('health.db', check_same_thread=False)
    conn.execute(f'''INSERT INTO health (id,status) VALUES ({user_id},'{status}')''')
    conn.commit()
    conn.close()
    return

def update_health(user_id:int,status:str):
    conn = sqlite3.connect('health.db', check_same_thread=False)
    conn.execute(f'''UPDATE health SET status='{status}' WHERE id={user_id}''')
    conn.commit()
    conn.close()
    return

def get_disease(user_id):
    conn = sqlite3.connect('health.db', check_same_thread=False)
    user = conn.execute(f'SELECT * FROM disease WHERE id ={user_id}').fetchone()
    conn.close()
    if user is None:
        return None
    else:
        user_1 = user[1]
        return user_1

def insert_disease(user_id:int,disease:str):
    conn = sqlite3.connect('health.db', check_same_thread=False)
    conn.execute(f'''INSERT INTO disease (id,disease) VALUES ({user_id},'{disease}')''')
    conn.commit()
    conn.close()
    return

def update_disease(user_id:int,disease:str):
    conn = sqlite3.connect('health.db', check_same_thread=False)
    conn.execute(f'''UPDATE disease SET disease='{disease}' WHERE id={user_id}''')
    conn.commit()
    conn.close()
    return

def get_list():
    conn = sqlite3.connect('health.db', check_same_thread=False)
    list_all = conn.execute(f'''Select FIO.first_name,FIO.last_name,health.status,coalesce(disease.disease,"")
                                from users
                                    left join health on health.id=users.user_id
                                    left join disease on disease.id=users.user_id
                                    left join FIO on FIO.user_id=users.user_id
                                    left join id_status on id_status.user_id=users.user_id
                                where id_status.enable_report''').fetchall()
    conn.close()
    return list_all

def get_list_all():
    conn = sqlite3.connect('health.db', check_same_thread=False)
    list_all = conn.execute(f'''Select users.id,FIO.first_name,FIO.last_name,id_status.enable_report
                                from users
                                    left join FIO on FIO.user_id=users.user_id
                                    left join id_status on id_status.user_id=users.user_id
                                order by users.id''').fetchall()
    conn.close()
    return list_all

