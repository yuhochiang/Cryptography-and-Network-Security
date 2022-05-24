import socket
import operator
import base64
    
def replace(cipher, plain):
    for k,v in key.items():
        if k == cipher:
            tmp = key[k]
            key[k] = plain
    for k,v in key.items():
        if v == plain and k != cipher:
            key[k] = tmp

addr = ('140.114.77.172', 60003)
cipher = ''
unifreq = {}
bifreq = {}
trifreq = {}
quafreq = {}
#----------------------------------------------------------------#
#---------------------------Not base64---------------------------#
#----------------------------------------------------------------#
while (len(cipher) < 8000):
    sock = socket.socket()
    sock.connect(addr)
    msg = sock.recv(128)
    sock.send(b'105021221\n')
    msg = sock.recv(128)
    sock.send(b'n\n')
    msg = sock.recv(16384)
    msg = msg.decode()
    flag = msg[15:31]
    cipher = msg[32:]
    sock.close()

cipher1 = cipher.lower()
print('{' + flag + '}')
print(cipher)
for i in range(len(cipher1)):
    unifreq[cipher1[i]] = unifreq.get(cipher1[i], 0) + 1
    if i < len(cipher1) - 2:
        bifreq[cipher1[i:i+3]] = bifreq.get(cipher1[i:i+3], 0) + 1
    if i < len(cipher1) - 3:
        trifreq[cipher1[i:i+3]] = trifreq.get(cipher1[i:i+3], 0) + 1 
    if i < len(cipher1) - 4:
        quafreq[cipher1[i:i+4]] = quafreq.get(cipher1[i:i+4], 0) + 1

k = 'etaoinshrdlucmfwgypbvkxjqz'
for i in k:
    if i not in unifreq.keys():
        unifreq.update({i:0})
for i in unifreq.keys():
    if i not in k:
        del unifreq[i]
        break

unifreq = sorted(unifreq.items(),key = operator.itemgetter(1),reverse = True)
bifreq = sorted(bifreq.items(),key = operator.itemgetter(1),reverse = True)
trifreq = sorted(trifreq.items(),key = operator.itemgetter(1),reverse = True)
quafreq = sorted(quafreq.items(),key = operator.itemgetter(1),reverse = True)

#print(len(unifreq), unifreq)
#print(bifreq[0:5])
#print(trifreq[0:10])
#print(quafreq[0:10])

key = {unifreq[i][0] : k[i] for i in range(len(unifreq))}
replace(flag[0].lower(), 'b')
replace(flag[3].lower(), 'y')
replace(flag[5].lower(), 'm')
replace(flag[6].lower(), 'j')
replace(flag[9].lower(), 'x')
#print(key)

#to record which letter is found
found = {'b':flag[0].lower(), 'y':flag[3].lower(), 'm':flag[5].lower(), 'j':flag[6].lower(), 'x':flag[9].lower()}

#find t, h, e
for i in trifreq:
    if i[0][2] == unifreq[0][0]:
        replace(i[0][0], 't')
        replace(i[0][1], 'h')
        replace(i[0][2], 'e')
        found.update({'t':i[0][0], 'h':i[0][1], 'e':i[0][2]})
        break
#'and', 'ing' -> find n
for i in trifreq:
    if found['t'] not in i[0] and found['h'] not in i[0] and found['e'] not in i[0]:
        first_n = i[0]
        replace(i[0][1], 'n')
        found['n'] = i[0][1]
        break
for i in trifreq:
    if i[0][1] == found['n'] and i[0] != first_n:
        sec_n = i[0]
        break
#'and, 'ing' -> find a, d, i, g
unifreq = dict(unifreq)
if unifreq[first_n[2]] > unifreq[sec_n[2]]:
    replace(first_n[0], 'a')
    replace(first_n[2], 'd')
    replace(sec_n[0], 'i')
    replace(sec_n[2], 'g')
    found.update({'a':first_n[0], 'd':first_n[2], 'i':sec_n[0], 'g':sec_n[2]})
else:
    replace(sec_n[0], 'a')
    replace(sec_n[2], 'd')
    replace(first_n[0], 'i')
    replace(first_n[2], 'g')
    found.update({'a':sec_n[0], 'd':sec_n[2], 'i':first_n[0], 'g':first_n[2]})
#print(found)
#'ere' -> find r
unifreq = list(unifreq)
for i in trifreq:
    if i[0][0] == found['e'] and i[0][2] == found['e'] and i[0][1] not in found.values():
        replace(i[0][1], 'r')
        found['r'] = i[0][1]
        break
#'with' -> find w
for i in quafreq:
    if i[0][1] == found['i'] and i[0][2] == found['t'] and i[0][3] == found['h'] and i[0][0] not in found.values():
        replace(i[0][0], 'w')
        found['w'] = i[0][0]
        break
#'his' -> find s
for i in trifreq:
    if i[0][0] == found['h'] and i[0][1] == found['i'] and i[0][2] not in found.values():
        replace(i[0][2], 's')
        found['s'] = i[0][2]
        break
replace(flag[2].lower(), 'w')
found['w'] = flag[2].lower()
if 's' not in found.keys():
    for i in trifreq:
        if i[0][0] == found['w'] and i[0][1] == found['a'] and i[0][2] not in found.values():
            replace(i[0][2], 's')
            found['s'] = i[0][2]
            break
#find o
for i in unifreq:
    if i[0] not in found.values():
        replace(i[0], 'o')
        found['o'] = i[0]
        break
#'ou' -> find u
for i in bifreq:
    if i[0][0] == found['o'] and i[0][1] not in found.values():
        replace(i[0][1], 'u')
        found['u'] = i[0][1]
        break
#find l
if 'l' not in found.keys():
    for i in unifreq:
        if i[0] not in found.values():
            replace(i[0], 'l')
            found['l'] = i[0]
            break
#'all' -> find l
if 'l' not in found.keys():
    for i in trifreq:
        if i[0][0] == found['a'] and i[0][1] == i[0][2] and i[0][1] not in found.values():
            replace(i[0][0], 'l')
            found['l'] = i[0][0]
            break
#'for' -> find f
for i in trifreq:
    if i[0][1] == found['o'] and i[0][2] == found['r'] and i[0][0] not in found.values():
        replace(i[0][0], 'f')
        found['f'] = i[0][0]
        break
#'have' -> find v
for i in quafreq:
    if i[0][0] == found['h'] and i[0][1] == found['a'] and i[0][3] == found['e'] and i[0][2] not in found.values():
        if i[0][2] == flag[-5].lower:
            replace(i[0][2], 'v')
            found['v'] = i[0][2]
            break
        else:
            replace(flag[-5].lower(), 'v')
            found['v'] = flag[-5].lower()
#'coul'-> find c
for i in quafreq:
    if i[0][1] == found['o'] and i[0][2] == found['u'] and i[0][3] == found['l'] and i[0][0] not in found.values():
        replace(i[0][0], 'c')
        found['c'] = i[0][0]
        break
#'whic' -> find c
if 'c' not in found.keys():
    for i in quafreq:
        if i[0][0] == found['w'] and i[0][1] == found['h'] and i[0][2] == found['i'] and i[0][3] not in found.values():
            found['c'] = i[0][3]
            replace(i[0][3], 'c')
            break
#'ence' -> find c
if 'c' not in found.keys():
    for i in quafreq:
        if i[0][0] == found['e'] and i[0][1] == found['n'] and i[0][3] == found['e'] and i[0][3] not in found.values():
            found['c'] = i[0][2]
            replace(i[0][2], 'c')
            break
#'you' -> find y
if 'y' not in found.keys():
    for i in trifreq:
        if i[0][1] == found['o'] and i[0][2] == found['u'] and i[0][0] not in found.values():
            replace(i[0][0], 'y')
            found['y'] = i[0][0]
            break
#'from' -> find f
for i in quafreq:
    if 'f' not in found.keys():
        if i[0][0] not in found.values() and i[0][1] == found['r'] and i[0][2] == found['o'] and i[0][3] not in found.values():
            replace(i[0][0], 'f')
            found['f'] = i[0][0]
            break
replace(flag[-3].lower(), 'p')
found['p'] = flag[-3].lower()
#'of' -> find f
if 'f' not in found.keys():
    for i in bifreq:
        if i[0][0] == found['o'] and i[0][1] not in found.values():
            replace(i[0][1], 'f')
            found['f'] = i[0][1]
            break
#'pl' -> find p
if 'p' not in found.keys():
    for i in bifreq:
        if i[0][1] == found['l'] and i[0][0] not in found.values():
            replace(i[0][0], 'p')
            found['p'] = i[0][0]
            break
#'pro' -> find p
if 'p' not in found.keys():
    for i in trifreq:
        if i[0][1] == found['r'] and i[0][2] == found['o'] and i[0][0] not in found.values():
            found['p'] = i[0][0]
            replace(i[0][0], 'p')
            break
#'uppo' -> find p
if 'p' not in found.keys():
    for i in quafreq:
        if i[0][0] == found['u'] and i[0][3] == found['o'] and i[0][1] == i[0][2] and i[0][2] not in found.values():
            found['p'] = i[0][1]
            replace(i[0][1], 'p')
            break
#'peop' -> find p
if 'p' not in found.keys():
    for i in quafreq:
        if i[0][1] == found['e'] and i[0][2] == found['o'] and i[0][0] == i[0][3] and i[0][3] not in found.values():
            found['p'] = i[0][0]
            replace(i[0][0], 'p')
            break
#'about' -> find b
if 'b' not in found.keys():    
    for i in quafreq:
        if i[0][0] == found['a'] and i[0][2] == found['o'] and i[0][3] == found['u'] and i[0][1] not in found.values():
            found['b'] = i[0][1]
            replace(i[0][1], 'b')
            break
#'but' -> find b
if 'b' not in found.keys():
    for i in trifreq:
        if i[0][1] == found['u'] and i[0][2] == found['t'] and i[0][0] not in found.values():
            found['b'] = i[0][0]
            replace(i[0][0], 'b')
            break
#'just' -> find j
if 'j' not in found.keys():
    for i in quafreq:
        if i[0][1] == found['u'] and i[0][2] == found['s'] and i[0][3] == found['t'] and i[0][0] not in found.values():
            found['j'] = i[0][0]
            replace(i[0][0], 'j')
            break
#'king' -> find k
for i in quafreq:
    if i[0][1] == found['i'] and i[0][2] == found['n'] and i[0][3] == found['g'] and i[0][0] not in found.values():
        replace(i[0][0], 'k')
        found['k'] = i[0][0]
        break
#'que' -> find q
for i in trifreq:
    if i[0][1] == found['u'] and i[0][2] == found['e'] and i[0][0] not in found.values():
        replace(i[0][0], 'q')
        found['q'] = i[0][0]
        break
#'ize' -> find z
for i in trifreq:
    if i[0][0] == found['i'] and i[0][2] == found['e'] and i[0][1] not in found.values():
        replace(i[0][1], 'z')
        found['z'] = i[0][1]
        break
#'uzzl' -> find z
for i in quafreq:
    if i[0][0] == found['u'] and i[0][3] == found['l'] and i[0][1] == i[0][2] and i[0][1] not in found.values():
        replace(i[0][1], 'z')
        found['z'] = i[0][1]
        break
        
#print(found.keys())
#print(key)
plain = ''
flaggg = ''
ans = ''
for i in cipher[:-1]:
    if i.islower():
        plain += key[i]
    else:
        plain += key[i.lower()].upper()

for i in flag:
    flaggg += key[i.lower()].upper()

for i in 'abcdefghijklmnopqrstuvwxyz':
    ans += key.get(i).upper()

print('\n')
print('flag:', '{' + flaggg + '}')
print('key:', ans)
print('\n')
print(plain)
print('\n\n\n')

#----------------------------------------------------------------#
#-----------------------------base64-----------------------------#
#----------------------------------------------------------------#
cipher = ''
while (len(cipher) < 7000):
    sock = socket.socket()
    sock.connect(addr)
    msg = sock.recv(128)
    sock.send(b'105021221\n')
    msg = sock.recv(128)
    sock.send(b'y\n')
    msg = sock.recv(16384)
    msg = msg.decode()
    cipher = msg[14:]
    sock.close()

freq1st = {}
freq3rd = {}
freq4 = {}
print(cipher)
print('\n\n\n')
for i in range(0, len(cipher), 4):      # 1st in base64
    if cipher[i].isalpha():
        freq1st[cipher[i]] = freq1st.get(cipher[i], 0) + 1
for i in range(3, len(cipher), 4):
    if cipher[i].isalpha() and cipher[i].islower():     #3rd in utf8 -> 4th in base64
        freq3rd[cipher[i]] = freq3rd.get(cipher[i], 0) + 1
for i in range(0, len(cipher)-1, 4):
    if cipher[i].isalpha():
        s = cipher[i:i+4]
        if len(s) != 4:
            break
        else:
            freq4[s] = freq4.get(s, 0) + 1

freq1st = sorted(freq1st.items(),key = operator.itemgetter(1),reverse = True)
freq3rd = sorted(freq3rd.items(),key = operator.itemgetter(1),reverse = True)
freq4 = sorted(freq4.items(),key = operator.itemgetter(1),reverse = True)

#print(freq1st)
#print(freq3rd[:10])
#print(freq4[:10])
found = {}
for i in '0123456789':
    key[i] = i
    found[i] = i
#print(key)
#{ -> find e
replace(cipher[0], 'e')
found['e'] = cipher[0]

# freq3rd
# 4th character in base64
# A->B, B->C, C->D,...,Y->Z, Z->a, a->h, b->i,...,s->z, t->0, u->1,..., z->6

# e -> find l
replace(freq3rd[0][0], 'l')
found['l'] = freq3rd[0][0]

# freq1st
# a,b,c   -> Y  | l,m,n,o -> b  | x,y,z,{ -> e      
# d,e,f,g -> Z  | p,q,r,s -> c  |
# h,i,j,k -> a  | t,u,v,w -> d  |

# d, e, f, g -> find Z
for i in freq1st:
    if i[0].isupper():
        replace(i[0].lower(), 'z')
        found['z'] = i[0].lower()
        break
# a, b, c -> find Y
for i in freq1st:
    if i[0].isupper() and i[0].lower() not in found.values():
        replace(i[0].lower(), 'y')
        found['y'] = i[0].lower()
        break
# l, m, n, o -> find b
for i in freq1st:
    if i[0].islower() and i[0] not in found.values():
        replace(i[0], 'b')
        found['b'] = i[0]
        break
# use the same way in utf8 version
# the -> dGhl   | his -> aGlz   | ion -> aW9u   | ver -> dmVy
# and -> YW5k   | tha -> dGhh   | ter -> dGVy   | all -> YWxs
# ing -> aW5n   | ere -> ZXJl   | was -> d2Fz   | wit -> d2l0
# her -> aGVy   | for -> Zm9y   | you -> eW91   | thi -> dGhp
# hat -> aGF0   | ent -> ZW50   | ith -> aXRo   | tio -> dGlv

# the -> dGhl -> find d, g, h
for i in freq4:
    if i[0][0].islower() and i[0][0] not in found.values() and \
        i[0][1].isupper() and i[0][1].lower() not in found.values() and \
        i[0][2].islower() and i[0][2] not in found.values() and i[0][3] == found['l']:
        replace(i[0][0], 'd')
        replace(i[0][1].lower(), 'g')
        replace(i[0][2], 'h')
        found.update({'d':i[0][0], 'g':i[0][1].lower(), 'h':i[0][2]})
        break
# and -> YW5k -> find w, k
for i in freq4:
    if i[0][0].isupper() and i[0][0].lower() == found['y'] and \
        i[0][1].isupper() and i[0][1].lower() not in found.values() and \
        i[0][2] == found['5'] and i[0][3].islower() and i[0][3] not in found.values():
        replace(i[0][1].lower(), 'w')
        replace(i[0][3], 'k')
        found.update({'w':i[0][1].lower(), 'k':i[0][3]})
        break
# ing -> aW5n -> find a, n
for i in freq4:
    if i[0][0].islower() and i[0][0] not in found.values() and \
        i[0][1].isupper() and i[0][1].lower() == found['w'] and \
        i[0][2] == found['5'] and i[0][3].islower() and i[0][3] not in found.values():
        replace(i[0][0], 'a')
        replace(i[0][3], 'n')
        found.update({'a':i[0][0], 'n':i[0][3]})
        break
# find c
for i in freq1st:
    if i[0].islower() and i[0] not in found.values():
        replace(i[0], 'c')
        found['c'] = i[0]
# her -> aGVy -> find v
for i in freq4:
    if i[0][0].islower() and i[0][0] == found['a'] and \
        i[0][1].isupper() and i[0][1].lower() == found['g'] and \
        i[0][2].isupper() and i[0][2].lower() not in found.values() and \
        i[0][3].islower() and i[0][3] == found['y']:
        replace(i[0][2].lower(), 'v')
        found['v'] = i[0][2].lower()
        break
# hat -> aGF0 -> find f
for i in freq4:
    if i[0][0].islower() and i[0][0] == found['a'] and \
        i[0][1].isupper() and i[0][1].lower() == found['g'] and \
        i[0][2].isupper() and i[0][2].lower() not in found.values() and i[0][3] == found['0']:
        replace(i[0][2].lower(), 'f')
        found['f'] = i[0][2].lower()
        break
# was -> d2Fz -> find f
if 'f' not in found.keys():
    for i in freq4:
        if i[0][0].islower() and i[0][0] == found['d'] and i[0][1] == found['2'] and \
            i[0][2].isupper() and i[0][2].lower() not in found.values() and i[0][3] == found['z']:
            replace(i[0][2].lower(), 'f')
            found['f'] = i[0][2].lower()
            break
# ere -> ZXJl -> find x, j
for i in freq4:
    if i[0][0].isupper() and i[0][0].lower() == found['z'] and \
        i[0][1].isupper() and i[0][1].lower() not in found.values() and \
        i[0][2].isupper() and i[0][2].lower() not in found.values() and i[0][3] == found['l']:
        replace(i[0][1].lower(), 'x')
        replace(i[0][2].lower(), 'j')
        found.update({'x':i[0][1].lower(), 'j':i[0][2].lower()})
        break
# for -> Zm9y -> find m
for i in freq4:
    if i[0][0].isupper() and i[0][0].lower() == found['z'] and \
        i[0][1].islower() and i[0][1] not in found.values() and \
        i[0][2] == found['9'] and i[0][3] == found['y']:
        replace(i[0][1], 'm')
        found['m'] = i[0][1]
        break
# ver -> dmVy -> find m
if 'm' not in found.keys():
    for i in freq4:
        if i[0][0].islower() and i[0][0] == found['d'] and \
            i[0][1].islower() and i[0][1] not in found.values() and \
            i[0][2].isupper() and i[0][2].lower() == found['v'] and i[0][3] == found['y']:
            replace(i[0][1], 'm')
            found['m'] = i[0][1]
            break
# in freq1st
# j -> q, k -> r, l -> s, m -> t, n -> u
# frequency: n > l > m > k > j
qrstu = set()      # to find which letter corresponding to qrstu
for i in freq1st:
    if i[0].isupper() and i[0].lower() not in found.values():
        qrstu.add(i[0].lower())
# n -> find u
for i in freq3rd:
    if i[0] in qrstu:
        replace(i[0], 'u')
        found['u'] = i[0]
        qrstu.remove(i[0])
        break
# l -> find s
for i in freq3rd:
    if i[0] in qrstu:
        replace(i[0], 's')
        found['s'] = i[0]
        qrstu.remove(i[0])
        break
# m -> find t
for i in freq3rd:
    if i[0] in qrstu:
        replace(i[0], 't')
        found['t'] = i[0]
        qrstu.remove(i[0])
        break
# k -> find r
for i in freq3rd:
    if i[0] in qrstu:
        replace(i[0], 'r')
        found['r'] = i[0]
        qrstu.remove(i[0])
        break
# j -> find q
for i in freq3rd:
    if i[0] in qrstu:
        replace(i[0], 'q')
        found['q'] = i[0]
        qrstu.remove(i[0])
        break
# ith -> aXRo -> find x
if 'x' not in found.keys():
    for i in freq4:
        if i[0][0].islower() and i[0][0] == found['a'] and \
            i[0][1].isupper() and i[0][0].lower() not in found.values() and \
            i[0][2].isupper() and i[0][2].lower() == found['r'] and \
            i[0][3].islower() and i[0][3] not in found.values():
            replace(i[0][1].lower(), 'x')
            replace(i[0][3], 'o')
            found.update({'x':i[0][1].lower(), 'o':i[0][3]})
            break
# all -> YWxs -> find x
if 'x' not in found.keys():
    for i in freq4:
        if i[0][0].isupper() and i[0][0].lower() == found['y'] and \
            i[0][1].isupper() and i[0][1].lower() == found['w'] and \
            i[0][2].islower() and i[0][2] not in found.values() and i[0][3] == found['s']:
            replace(i[0][2], 'x')
            found['x'] = i[0][2]
            break
# found a, b, c, d, e, f, g, h, j, k, l, m, n, q, r, s, t, u, v, w, x, y, z
# remain i, j, o, p
# in freq3rd b->i, c->j, h->o, i->p

# find i
for i in freq3rd[::-1]:
    if i[0] and i[0] not in found.values():
        replace(i[0], 'i')
        found['i'] = i[0]
        print()
        break
# find j
if 'j' not in found.keys():
    for i in freq3rd[::-1]:
        if i[0] and i[0] not in found.values():
            replace(i[0], 'j')
            found['j'] = i[0]
            break
# ith -> aXRo -> find o
if 'o' not in found.keys():
    for i in freq4:
        if i[0][0].islower() and i[0][0] == found['a'] and \
            i[0][1].isupper() and i[0][1].lower() == found['x'] and \
            i[0][2].isupper() and i[0][2].lower() == found['r'] and \
            i[0][3].islower() and i[0][3] not in found.values():
            replace(i[0][3], 'o')
            found['o'] = i[0][3]
            break
if 'q' not in found.keys():
    # thi -> dGhp -> find p
    for i in freq4:
        if i[0][0].islower() and i[0][0] == found['d'] and \
            i[0][1].isupper() and i[0][1].lower() == found['g'] and \
            i[0][2].islower() and i[0][2] == found['h'] and \
            i[0][3].islower() and i[0][3] not in found.values():
            replace(i[0][3], 'p')
            found['p'] = i[0][3]
            break
    # find q
    for i in 'abcdefghijklmnopqrstuvwxyz':
        if i not in found.values():
            replace(i, 'q')
            found['q'] = i
            break
else:
    # find p
    for i in 'abcdefghijklmnopqrstuvwxyz':
        if i not in found.values():
            replace(i, 'p')
            found['p'] = i
            break
plain = ''
flaggg = ''
ans = ''
for i in cipher:
    if i.isalpha() and i.isupper():
        plain += key[i.lower()].upper()
    elif i == '\n':
        continue
    else:
        plain += key[i]

for i in 'abcdefghijklmnopqrstuvwxyz':
    ans += key.get(i).upper()

print('base64 key:', ans)
print('base64 plaintext:', plain)
print('\n\n\n')
plain += "=" * (4 - len(plain) % 4)
plain = plain.encode()
plain = base64.b64decode(plain)
print('utf-8 plaintext:', str(plain).split("'")[1])
