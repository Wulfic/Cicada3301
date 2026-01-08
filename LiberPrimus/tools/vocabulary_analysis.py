
import os
import re
from collections import Counter

# Manually load the decrypted text I just found (or read from files)
# I'll rely on the text I generated in the previous step
PAGES = {
    1: """iaeoseia-niaoþeomij.iþeiaþeoþi-pbþ
u-uciþeþ-eopeoŋ.oea-þeaþ-ean-oþeocc
etmþ-eoneaaþea-þeaea-xl-ui-tunff-þ
eæ-iawþæ-œwþ-eiau-apœe-pþ.æ-lþ-
aœ-gxn-ibœleoa-weoxheap-hryleoþ
-eoxheaoþþ-eaþeþeþ-edþean.leoi-cæ
þetsaþeod-gl-eoiagmþe-theo-œi
iiwa-þelþeoþeoxx.nuu-þeaþ-eaf
iadat-gx-ean-þeoeolwsf-yœ-œn-nl
mþ-eaealeaþyþ-eoal-wfþ-eoþeþeo-g
þeo-mþeagþ-eaeo-mp-þeo-þeacyeaþ-eau
bþ-eþæic-heu-fuc-peþeomŋm-xuj""",

    2: """ta-þ.eat-heoœþeopp-gþea-fþeagŋf-
æjeoxjþe-aþeo-æwþeaþ-eomþeo-lþeaþe
hu-fihæþeoeaœþea-þeþalcþ-eþ-þ
eoþeouin-gþaeoþeþ-ealþeaþ-eagþx-ŋþea
œþþeo-txuilþ-earþeanæþeþ-eolŋ-g
þ-ia-þeþeœaþea-œuiaþeaþeoþea-lh
eaþed-ieatþeþeawææ-þxrþ-eaþeo-dþeo
tuypþ-aþheaiaæþe-dwia-eam-þe-eaþ
eaeoþþeomþe-þeo-ynæjxþeoeaæ.""",
    
    4: """bia-ŋiþeowgeal-þætlþeaa-ngþr-þ-eo
m-hlw-uileodia-ŋgh-baþ-ealeo
i-sþ-eoæ-þea-taaþ-þeœycœ-rþ-el
eit-lmoþeaþ-tþþeodf.þ-eæpo-þwy-
mui-þf-th-exa-þmu.iaþeoþ-eol
eþeaþ-eaæh-eteo-þ-eopþeo.pjufþ
eathþ-earl-eatti-þealþeao-ŋfxo-þ
eœs-þeodþealteaþea-snœeo.þeoœxgŋ
lbþ-eayþeo-þearheolþea-eh-cgþex
iþæg-þeojl-þea-wœþ-emcuythi-l
eaeaþea-þauixth-ealþ-eaoþeaþ-eaifh-
bþeolybþeæþ-ebþea-þeþeoe-heaþ-l""",

    5: """lþ-eaniaŋœa-llj-geon-þjpœlxlþ-
eatsþ-eotæþeaþ-eaþea-mpx-diamþ-e-
þyiarub-þeani-lmw-þeþ-eom-uiþ
eeajþxl-eaþea-pmþea-þeam-þeofþeo.gd
na-ejineapþ-heaþ-eoixthinæ-u.
ceo-deop-þeoi-leohea-þeoeþeœŋo-iw
þ-efbe-œydj-easœuiaiaþiia-he
þeþeo-iadaþea-þeod-orŋa-eoœteoþpþ-
tþeda-þeþeamu-eal-þagnuiþ-jþ
eau-þeaeabtþeoþea-þeaþeonwæþeaw-e
æ.leaþea-peaiwþeas-leaþpþe-þeag-du
þrgr-þeoaþ-eaœu-ieæ-œsh-hþ-eo"""
}

# Common Old English / Runeglish Words (Hypothesis)
COMMON_WORDS = {
    'þe', 'ea', 'eo', 'aþ', 'oþ', 'an', 'is', 'it', 'in', 'on', 'to', 'of', 'at', 
    'se', 'swa', 'ne', 'mid', 'for', 'be', 'ic', 'he', 'we', 'ge', 'hi',
    'and', 'wiþ', 'eal', 'eall', 'dœþ', 'fleþ', 'waron', 'þær', 'þa', 'þu', 'min'
}

def analyze_vocabulary():
    all_words = []
    
    for page, text in PAGES.items():
        # clean text: remove dots, newlines, treat hyphens as split
        clean_text = text.replace('.', ' ').replace('\n', ' ')
        words = [w.strip() for w in clean_text.split('-') if w.strip()]
        all_words.extend(words)
        
    counts = Counter(all_words)
    
    print(f"Total Words Found: {len(all_words)}")
    print(f"Unique Words: {len(counts)}")
    print("\nTop 20 Frequent Words:")
    for w, c in counts.most_common(20):
        print(f"{w}: {c}")
        
    # Overlap with common hypothesis
    print("\nMatches with Known Old English Particles:")
    matches = 0
    for w in counts:
        if w in COMMON_WORDS:
            print(f"MATCH: {w} ({counts[w]})")
            matches += 1
            
    print(f"\nTotal Dictionary Matches: {matches}")
    
    # Identify single letters (runes acting as logograms?)
    singles = [w for w in counts if len(w) == 1]
    print(f"\nSingle Letter Words: {singles}")
    
    # Check for specific Page 0 words
    p0_words = {'fleþ', 'eall', 'uile', 'dœþ', 'warn', 'wylc'}
    print("\nPage 0 Vocab Check:")
    for w in p0_words:
        if w in counts:
            print(f"FOUND P0 WORD: {w}")

if __name__ == "__main__":
    analyze_vocabulary()
