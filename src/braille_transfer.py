import hbcvt

def main(place="서울 도서관"):
    rkrk = []
    
    for i in hbcvt.h2b.text(place):
        for j in i[1:]:
            for k in j:
                rkrk.append(k[1:][0][0])
    return rkrk

def number_transfer(number=0):
    return  hbcvt.h2b.MATCH_H2B_ALPHABET[str(number)]
