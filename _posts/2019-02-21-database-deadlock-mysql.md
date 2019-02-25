---
layout: post
comments: true
title: MySQL - Navigating through deadlock minefield
description: How we solved an interesting deadlock error in MySql
---

{{ page.title }}
================

<p class="meta">
    Saptarshi Chatterjee 
</p>

---

For most of our microservices, we are using MySQL as our primary DB Server. In this blog I'll describe an interesting deadlock issue we faced in MySQL and the solution we went for.

The story started one day with our SSO server logging errors related to deadlock. Here is the stacktrace-
```
Caused by: com.mysql.jdbc.exceptions.jdbc4.MySQLTransactionRollbackException: 
Deadlock found when trying to get lock; 
try restarting transaction
	at sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)
	at sun.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:62)
	at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)
	at java.lang.reflect.Constructor.newInstance(Constructor.java:423)
	at com.mysql.jdbc.Util.handleNewInstance(Util.java:425)
```

We immediately started digging MySql server and got more details on the situation.

Command we ran: `show engine innodb status`

Output we got:
```
=====================================
2019-02-08 20:17:16 0x70000114d000 INNODB MONITOR OUTPUT
=====================================
Per second averages calculated from the last 56 seconds
-----------------
BACKGROUND THREAD
-----------------
srv_master_thread loops: 18 srv_active, 0 srv_shutdown, 2425 srv_idle
srv_master_thread log flush and writes: 2443
----------
SEMAPHORES
----------
OS WAIT ARRAY INFO: reservation count 44
OS WAIT ARRAY INFO: signal count 44
RW-shared spins 0, rounds 57, OS waits 27
RW-excl spins 0, rounds 30, OS waits 0
RW-sx spins 0, rounds 0, OS waits 0
Spin rounds per wait: 57.00 RW-shared, 30.00 RW-excl, 0.00 RW-sx
------------------------
LATEST DETECTED DEADLOCK
------------------------
2019-02-08 19:39:57 0x700000ee9000
*** (1) TRANSACTION:
TRANSACTION 15894, ACTIVE 2 sec starting index read
mysql tables in use 1, locked 1
LOCK WAIT 5 lock struct(s), heap size 1136, 2 row lock(s), undo log entries 1
MySQL thread id 339, OS thread handle 123145316552704, query id 431 localhost 127.0.0.1 ssouser updating
update t_users set last_login_on='2019-02-08 14:09:57.447' where id=316
*** (1) WAITING FOR THIS LOCK TO BE GRANTED:
RECORD LOCKS space id 133 page no 12 n bits 128 index PRIMARY of table `sso`.`t_users` trx id 15894 lock_mode X locks rec but not gap waiting
Record lock, heap no 28 PHYSICAL RECORD: n_fields 31; compact format; info bits 0
 0: len 4; hex 0000013c; asc    <;;
 1: len 6; hex 000000003e14; asc     > ;;
 2: len 7; hex 310000013e223f; asc 1   >"?;;
 3: len 18; hex 617368697276616440676d61696c2e636f6d; asc ashirvad@gmail.com;;
 4: len 8; hex 4153484952564144; asc ASHIRVAD;;
 5: len 8; hex 4153484952564144; asc ASHIRVAD;;
 6: len 18; hex 617368697276616440676d61696c2e636f6d; asc ashirvad@gmail.com;;
 7: len 10; hex 39363332353837343532; asc 9632587452;;
 8: len 10; hex 39363332353837343532; asc 9632587452;;
 9: len 5; hex 99a09c4db9; asc    M ;;
 10: len 30; hex 243261243130246c704e5355553536596f694444396d4b44566663692e4f; asc $2a$10$lpNSUU56YoiDD9mKDVfci.O; (total 60 bytes);
 11: len 4; hex 5c5d3f75; asc \]?u;;
 12: SQL NULL;
 13: SQL NULL;
 14: len 4; hex 5b7260a2; asc [r` ;;
 15: SQL NULL;
 16: len 4; hex 5c3c2792; asc \<' ;;
 17: len 4; hex 0000013c; asc    <;;
 18: len 1; hex 80; asc  ;;
 19: len 4; hex 0000007f; asc     ;;
 20: len 1; hex 48; asc H;;
 21: SQL NULL;
 22: SQL NULL;
 23: SQL NULL;
 24: SQL NULL;
 25: SQL NULL;
 26: SQL NULL;
 27: len 1; hex 49; asc I;;
 28: len 30; hex 56454c34726847376d4c654e345064315844614e6e664f33464d3850366e; asc VEL4rhG7mLeN4Pd1XDaNnfO3FM8P6n; (total 64 bytes);
 29: len 4; hex 80000000; asc     ;;
 30: SQL NULL;

*** (2) TRANSACTION:
TRANSACTION 15895, ACTIVE 2 sec starting index read
mysql tables in use 1, locked 1
5 lock struct(s), heap size 1136, 2 row lock(s), undo log entries 1
MySQL thread id 338, OS thread handle 123145317945344, query id 430 localhost 127.0.0.1 ssouser updating
update t_users set last_login_on='2019-02-08 14:09:57.447' where id=316
*** (2) HOLDS THE LOCK(S):
RECORD LOCKS space id 133 page no 12 n bits 128 index PRIMARY of table `sso`.`t_users` trx id 15895 lock mode S locks rec but not gap
Record lock, heap no 28 PHYSICAL RECORD: n_fields 31; compact format; info bits 0
 0: len 4; hex 0000013c; asc    <;;
 1: len 6; hex 000000003e14; asc     > ;;
 2: len 7; hex 310000013e223f; asc 1   >"?;;
 3: len 18; hex 617368697276616440676d61696c2e636f6d; asc ashirvad@gmail.com;;
 4: len 8; hex 4153484952564144; asc ASHIRVAD;;
 5: len 8; hex 4153484952564144; asc ASHIRVAD;;
 6: len 18; hex 617368697276616440676d61696c2e636f6d; asc ashirvad@gmail.com;;
 7: len 10; hex 39363332353837343532; asc 9632587452;;
 8: len 10; hex 39363332353837343532; asc 9632587452;;
 9: len 5; hex 99a09c4db9; asc    M ;;
 10: len 30; hex 243261243130246c704e5355553536596f694444396d4b44566663692e4f; asc $2a$10$lpNSUU56YoiDD9mKDVfci.O; (total 60 bytes);
 11: len 4; hex 5c5d3f75; asc \]?u;;
 12: SQL NULL;
 13: SQL NULL;
 14: len 4; hex 5b7260a2; asc [r` ;;
 15: SQL NULL;
 16: len 4; hex 5c3c2792; asc \<' ;;
 17: len 4; hex 0000013c; asc    <;;
 18: len 1; hex 80; asc  ;;
 19: len 4; hex 0000007f; asc     ;;
 20: len 1; hex 48; asc H;;
 21: SQL NULL;
 22: SQL NULL;
 23: SQL NULL;
 24: SQL NULL;
 25: SQL NULL;
 26: SQL NULL;
 27: len 1; hex 49; asc I;;
 28: len 30; hex 56454c34726847376d4c654e345064315844614e6e664f33464d3850366e; asc VEL4rhG7mLeN4Pd1XDaNnfO3FM8P6n; (total 64 bytes);
 29: len 4; hex 80000000; asc     ;;
 30: SQL NULL;

*** (2) WAITING FOR THIS LOCK TO BE GRANTED:
RECORD LOCKS space id 133 page no 12 n bits 128 index PRIMARY of table `sso`.`t_users` trx id 15895 lock_mode X locks rec but not gap waiting
Record lock, heap no 28 PHYSICAL RECORD: n_fields 31; compact format; info bits 0
 0: len 4; hex 0000013c; asc    <;;
 1: len 6; hex 000000003e14; asc     > ;;
 2: len 7; hex 310000013e223f; asc 1   >"?;;
 3: len 18; hex 617368697276616440676d61696c2e636f6d; asc ashirvad@gmail.com;;
 4: len 8; hex 4153484952564144; asc ASHIRVAD;;
 5: len 8; hex 4153484952564144; asc ASHIRVAD;;
 6: len 18; hex 617368697276616440676d61696c2e636f6d; asc ashirvad@gmail.com;;
 7: len 10; hex 39363332353837343532; asc 9632587452;;
 8: len 10; hex 39363332353837343532; asc 9632587452;;
 9: len 5; hex 99a09c4db9; asc    M ;;
 10: len 30; hex 243261243130246c704e5355553536596f694444396d4b44566663692e4f; asc $2a$10$lpNSUU56YoiDD9mKDVfci.O; (total 60 bytes);
 11: len 4; hex 5c5d3f75; asc \]?u;;
 12: SQL NULL;
 13: SQL NULL;
 14: len 4; hex 5b7260a2; asc [r` ;;
 15: SQL NULL;
 16: len 4; hex 5c3c2792; asc \<' ;;
 17: len 4; hex 0000013c; asc    <;;
 18: len 1; hex 80; asc  ;;
 19: len 4; hex 0000007f; asc     ;;
 20: len 1; hex 48; asc H;;
 21: SQL NULL;
 22: SQL NULL;
 23: SQL NULL;
 24: SQL NULL;
 25: SQL NULL;
 26: SQL NULL;
 27: len 1; hex 49; asc I;;
 28: len 30; hex 56454c34726847376d4c654e345064315844614e6e664f33464d3850366e; asc VEL4rhG7mLeN4Pd1XDaNnfO3FM8P6n; (total 64 bytes);
 29: len 4; hex 80000000; asc     ;;
 30: SQL NULL;

*** WE ROLL BACK TRANSACTION (2)
```
Inference we made:
```
TRANSACTION (1):
    - Got exclusive lock on Primary Index of t_users

TRANSACTION (2):
    - Got Shared lock for Primary index of t_users
    - Waiting for exclusive lock on Primary Index of t_users

```

Immediate debugging revealed that this is happening when 2 clients are trying to request auth token from SSO server concurrently. 

Now we all know that deadlock can happen if 2 concurrent transactions are accessing 2 resources at reverse order.
For example deadloack can happen in below situation:
```
T1:
    BEGIN TRANSACTION
    INSERT TABLE A
    INSERT TABLE B
    END TRANSACTION

T2:
    BEGIN TRANSACTION
    INSERT TABLE B
    INSERT TABLE A
    END TRANSACTION
```

But.... here is the twist.
When our SSO server issues a token, it essentially does this 
``` 
    //Authenticate credentials
1.  BEGIN TRANSACTION
2.  Select from USER table 
3.  Validate password
4.  END TRANSACTION

    //Generate token
5.  BEGIN TRANSACTION
6.  Insert into TOKEN table

    //Update last login time
7.  SELECT from USER
8.  Update last_logintime in USER table
9.  END TRANSACTION
```
If you are paying attention so far you must have realized that there is no scope for reverse order execution here.  So what is going wrong here? 

To understand what is happening here, we have to understand relationship between `USER` and `TOKEN` table. The table relationship is like this:
``` sql
TOKEN.created_by => USER.id
```
This means `TOKEN` table has a foreign key relationship with `USER` table. In this relationship `USER` is parent and `TOKEN` is child.

So when 2 requests hit the server concurrently to generate token for the same user, both reach line-6 at the same time and and insert a row each in `TOKEN` table. While doing this, MYSql identifies that there is a FKEY relationship with USER table. So to protect integrity it acquires `SHARED` lock on that user's row in `USER` table for each request. 

Now one of the requests advances to line-8 and wants to update the same row in `USER` table with current time. For that it attempts to upgrade it's `SHARED` lock on `USER` table to `EXCLUSIVE` lock. But as request-2 is already holding a `SHARED` lock it waits for that lock to be released. In the meantime, request-2 advances to line-8 and attempts to acquire `EXCLUSIVE` lock which is already held by request-1. Now both are stuck .

Thankfully at this point MySql appears from sky and detects the situation as a deadlock and kills one transaction which results in application server stacktrace mentioned earlier.

---

### How to solve it and move forward?
Here are some of the solutions one can go for: 

**1. Remove referential integrity**

Remove referential integrity in the database. But purists like me won't like this as database sanity may go south after this.

**2. Retry transaction**

If failure is due to deadlock retry the transaction. Application frameworks should provide this functionality.

**3. Lock tables while updating**

Lock the update in child table by issuing SELECT for UPDATE. But it can impact performace significantly as all requests shall get serialized at this statement.

**4. Avoid the update in parent table after child**

Avoid the update in parent table when child table is already under attack. In our case we can avoid update in USER table at line-8 by performing this update just after line-3. 

That's all for today. Hope you liked it. :)

---

## PS
FYI. There is an option in MySQL to reduce transaction isolation level from `REPEATABLE-READ` to `READ-COMMITTED`. However it didn't work for us. You may try if you want. Caution: there is a [bug](https://bugs.mysql.com/bug.php?id=69800) in Mysql workbench which prevents it from showing updated transaction isolation level. Watch out for it if you are playing with this parameter. 


<p class="meta">
    Published on 21/Feb/2019
</p>
