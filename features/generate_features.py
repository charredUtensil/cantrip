import string
import glob
import os

def get_glyphs(directory_path):
    search_pattern = os.path.join(directory_path, '*.glyph')
    return [os.path.splitext(os.path.basename(file))[0].replace('_', '')
            for file in glob.glob(search_pattern)]

UNUSED = [
  'cmu', 'u1FB6C', 'u1FB6E', 'cantripVersion',
]
SPACE = [
  'space', 'hyphen', 'endash', 'emdash', 'underscore', 'periodcentered',
  'bullet',
]
DIGITS = [
  'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
  'nine',
]
SYMBOLS_NUMBERSIGN = [
  'asterisk', 'numbersign', 'percent', 'trademark', 'equal', 'at', 'plus',
  'copyright', 'greater', 'divide', 'less', 'degree', 'registered',
  'currency', 'plusminus', 'logicalnot', 'multiply', 'notequal', 'lessequal',
  'greaterequal',
]
SYMBOLS_OVER = [
  'acute', 'grave', 'asciicircum', 'asciitilde', 'dieresis', 'caron', 'ring',
  'macron', 'dotaccent', 'hungarumlaut', 'breve',
  'onesuper', 'twosuper', 'threesuper', 'ordmasculine', 'ordfeminine',
]
SYMBOLS = SYMBOLS_NUMBERSIGN + SYMBOLS_OVER + [
  'cedilla', 'ogonek',
  'cent', 'mu',
  'section', 'dollar', 'Euro', 'paragraph', 'yen', 'block', 'ampersand',
  'sterling',
  'onequarter', 'onehalf', 'threequarters', 'guillemotleft', 'guillemotright',
]
BARS = [
  'bar', 'brokenbar', 'parenleft', 'parenright', 'bracketleft', 'bracketright', 
  'braceleft', 'braceright', 'slash', 'backslash', 'dagger', 'daggerdbl',
  'florin',
]
PUNCTUATION = [
  'colon', 'semicolon', 'period', 'comma', 'exclam', 'exclamdown', 'question',
  'questiondown', 'ellipsis',
]
ACCENTS_OVER = [
  'acute', 'grave', 'circumflex', 'tilde', 'dieresis', 'caron', 'ring',
  'macron', 'dotaccent', 'hungarumlaut', 'breve', 'macron',
]
ACCENTS_UNDER = [
  'cedilla', 'ogonek',
]
OTHER_DIACRITICS = [
  'slash', 'bar', 'croat', 'dot',
]
OTHER_LETTERS = [
  'AE', 'ae', 'dotlessi', 'Eng', 'eng', 'Eth', 'eth', 'germandbls', 'IJ', 'ij',
  'OE', 'oe', 'Thorn', 'thorn',
]
LIGATURES = [
  'ii', 'll', 'tt', 'rr', 'mm', 'ww',
  'bs', 'gr', 'gs', 'is', 'ls', 'os', 'te', 'tr', 'ts',
  'tquotesingles',
]
WIDTH = [
  'wide', 'midwide', 'midthin', 'thin', 'proportional'
]
PARTS_AS_TAGS = [
  'short', 'proportional', 'cursive', 'lining',
] + WIDTH

# These don't follow convention for one reason or another.
OVERRIDES = {
  'Eth':          ['D',     'upper', 'diacritic',                                       ],
  'dcaron':       ['d',     'lower', 'diacritic',                                       ],
  'Eng':          ['Eng',   'upper', 'otherLetter',                       'descending', ],
  'eng':          ['eng',   'lower', 'otherLetter',                       'descending', ],
  'gcedilla':     ['g',     'lower', 'accentOver',                        'descending', ],
  'IJ':           ['IJ',    'upper', 'otherLetter',                       'descending', ],
  'ij':           ['ij',    'lower', 'otherLetter', 'accentOver',         'descending', ],
  'kgreenlandic': ['k',     'lower', 'diacritic',                                       ],
  'longs':        ['longs', 'lower', 'otherLetter',               'tall', 'descending', ],
  'Lcaron':       ['L',     'upper', 'diacritic',                                       ],
  'lcaron':       ['l',     'lower', 'diacritic',                 'tall',               ],
  'napostrophe':  ['n',     'lower', 'accentOver',                                      ],
  'tcaron':       ['t',     'lower', 'diacritic',                 'tall',               ],
  'thorn':        ['thorn', 'lower', 'otherletter',               'tall', 'descending', ]
}

def tags_for_letter(letter):
  tags = [letter]
  if letter[0].isupper():
    # upper case
    tags.append('upper')
  else:
    # lower case
    tags.append('lower')
  if len(letter) == 1:
    if letter in 'bdfhklt':
      # any lower case letter that extends above x is "tall"
      tags.append('tall')
    if letter in 'ij':
      # consider the dot above i and j to be an accent
      tags.append('accentOver')
    if letter in 'KRfgjkpqy':
      # anything that extends significantly below the base height

      # Consider all `j` to be descending, since they may be substituted for a
      # `j` that does. I don't want to complicate the logic.
      tags.append('descending')
  return tags

def tag_glyphs(glyphs):
  result = {}
  
  for glyph in glyphs:
    if glyph in OVERRIDES:
      result[glyph] = OVERRIDES[glyph]
      continue

    tags = []
    parts = glyph.split('.')
    base_glyph = parts[0]
    if base_glyph in UNUSED or base_glyph.startswith('unused'):
      continue
    elif 'hex' in parts:
      result[glyph] = ['digit', 'hex']
      continue
    elif base_glyph in SPACE:
      tags.extend([base_glyph, 'space'])
    elif base_glyph in DIGITS:
      tags.extend([base_glyph, 'digit'])
    elif base_glyph in SYMBOLS or base_glyph.startswith('SF') or base_glyph.startswith('uni'):
      tags.extend([base_glyph, 'symbol'])
    elif base_glyph in BARS:
      tags.extend([base_glyph, 'bar'])
    elif base_glyph in PUNCTUATION:
      tags.extend([base_glyph, 'punctuation'])
    elif base_glyph in LIGATURES:
      tags.extend([base_glyph, 'ligature'])
    elif len(base_glyph) == 1:
      tags.extend(tags_for_letter(base_glyph))
    elif base_glyph in OTHER_LETTERS:
      tags.extend(tags_for_letter(base_glyph))
      tags.append('otherLetter')
    elif base_glyph[1:] in ACCENTS_OVER:
      tags.extend(tags_for_letter(base_glyph[0]))
      tags.append('accentOver')
    elif base_glyph[1:] in ACCENTS_UNDER:
      tags.extend(tags_for_letter(base_glyph[0]))
      tags.append('accentUnder')
    elif base_glyph[1:] in OTHER_DIACRITICS:
      tags.extend(tags_for_letter(base_glyph[0]))
      tags.append('diacritic')
    elif base_glyph.startswith('quote'):
      tags.append('quotelike')
    else:
      raise RuntimeError(f'Unknown base glyph: {base_glyph}')

    tags.extend(p for p in parts if p in PARTS_AS_TAGS)
    
    if any(w in parts for w in WIDTH):
      # any glyph with a non-standard width
      tags.append('width')

    if 'sprawl' in parts:
      tags.append('sprawl')
      if 'sprawl.s' in glyph:
        tags.append('descending')

    result[glyph] = tags
        
  return result

def get_defs(tagged_glyphs):
  def matching(tags):
    return sorted(k for k in tagged_glyphs if all((
      (t[1:] not in tagged_glyphs[k]) if t.startswith('!') else (t in tagged_glyphs[k])
    ) for t in tags))
  def t(*tags):
    return ' '.join(matching(tags))
  def by(suffix, *tags):
    return '\n'.join(
      f'@{k}{suffix} = [{' '.join(v)}];'
      for k, v in ([k, matching((k,) + tags)] for k in string.ascii_uppercase + string.ascii_lowercase)
      if v)
  return f"""
###############################################################################
# DO NOT EDIT THIS FILE! It was generated by generate_features.py.            #
###############################################################################

###############################################################################
# Basic definitions that will be used elsewhere                               #
###############################################################################

# Individual letter kinds
{by('')}
{by('Cursive', 'cursive')}

# Digits
@digitsLining = [{t('digit', 'lining')}];
@digits = [{t('digit')}];

# Roughly bar shaped symbols (ascending + descending in the middle)
@bars = [{t('bar')}];

# Any punctuation
@punctuation = [{t('punctuation')}];

@commaLike = [
  comma comma.proportional
  semicolon semicolon.proportional
];

@upper = [{t('upper')}];

@lower = [{t('lower')}];
@xHeight = [{t('lower', '!tall', '!descending', '!accentOver', '!accentUnder')}];
@lowerNotTall = [{t('lower', '!tall')}];
@lowerNotDescending = [{t('lower', '!descending', '!accentUnder')}];
@lowerLeftTall = [@b @h @k @l {t('t', '!cursive')} germandbls thorn];
@lowerRightTall = [@d @f];

@flourishCompatSW = [
  {t('lower', '!descending', '!accentUnder', '!cursive', '!thin', '!midthin')}
];

# Misc incompatibilities
@blocksHex = [
  @G @H @I @J @K @L @M @N @O @P @Q @R @S @T @U @V @W @X @Y @Z
  @g @h @i @j @k @l @m @n @o @p @q @r @s @t @u @v @w @x @y @z
  {t('accentOver')}
  {t('accentUnder')}
  {t('diacritic')}
  {t('otherLetter')}
];
@blocksSprawlNW = [
  @digitsLining
  {t('upper', '!L')}
  @lowerRightTall
];
@blocksSprawlNWSwash = [
  @blocksSprawlNW
  {t('quotelike')}
];
@blocksSprawlNE = [
  @digitsLining
  @upper
  @lowerLeftTall
];
@blocksSprawlSW = [
  @K @R {t('Z', 'descending')} Eng IJ
  aogonek eogonek @g @j k.sprawl.se @q @tCursive @y {t('z', 'descending')} eng ij
];
@blocksSprawlSE.lower = [
  @A @L @M @W @X @Z IJ
  @f @g @j @p @y ij thorn
  @bars @commaLike slash
];
@blocksSprawlSE.upper = [
  @blocksSprawlSE.lower
  @B @C @D @E @F @I @H @J @K @N @P @R AE Eng
];
@blocksSprawlE.tCursive = [
  @upper @lower @digits @punctuation dollar Euro
];

# Digit groups (order matters)
@normalDigits = [
  zero one two three four five six seven eight nine
];
@liningDigits = [
  zero.lining one.lining two.lining three.lining four.lining
  five.lining six.lining seven.lining eight.lining nine.lining
];
@hexDigits = [
  zero.hex one.hex two.hex three.hex four.hex
  five.hex six.hex seven.hex eight.hex nine.hex
  a.hex b.hex c.hex d.hex e.hex f.hex
  A.hex B.hex C.hex D.hex E.hex F.hex
];
@hexable = [@normalDigits a b c d e f A B C D E F underscore];
@hexed = [@hexDigits underscore.hex];

@quotesingle = [quotesingle quotesingle.thin];

###############################################################################
# Lining Numerals                                                             #
###############################################################################

lookup lining {{
  {
    '\n'.join(
    f'sub {n} by {n}.lining;'
    for n
    in 'zero one two three four five six seven eight nine dollar Euro'.split())
  }
}} lining;

###############################################################################
# Replace hexadecimal literals with special glyphs                            #
###############################################################################

lookup toHex {{
    sub [ @hexable x X ] by [ @hexed x.hex X.hex ];
}} toHex;

lookup hexify {{
    # Any sequence of at least 2 hex digits prefixed with 0x, 0X, or #
    sub zero x' lookup toHex;
    sub zero X' lookup toHex;
    @prefix = [ x.hex X.hex numbersign ];

    # Ignore things that look too much like words.
    ignore sub {
      ', '.join(
        f"@prefix @hexable'{' '.join(('@hexable',) * i)} @blocksHex"
        for i in range(1, 8))
    };

    # Prefix followed by at least 2 hex digits
    sub @prefix @hexable' lookup toHex @hexable;

    # Any hexable digit following a hexed digit
    sub @hexed @hexable' lookup toHex;

    # Any sequence of at least 16 hexable digits
    sub @hexable' lookup toHex{ ' '.join(('@hexable',) * 15) };
}} hexify;

lookup afterHexify {{
  sub [x.hex X.hex]' by [x X];
}} afterHexify;

###############################################################################
# Cursive alternates                                                          #
###############################################################################

lookup toCursive {{
  sub e by e.cursive;
  sub g by g.cursive;
  sub S by S.cursive;
  sub s by s.cursive;
  sub t by t.cursive;
}} toCursive;

lookup cursiveAlts {{
  # e
  sub  [g.cursive @tCursive]  e' lookup toCursive;
  sub  b s.cursive            e' lookup toCursive;
  sub  o s.cursive            e' lookup toCursive;

  # g
  ignore sub g g';
  sub g' lookup toCursive                     [e r s];
  sub g' lookup toCursive g' lookup toCursive [e r s];
  sub [g.cursive @sCursive @tCursive] g' lookup toCursive;

  # S and s
  ignore sub s' s, s s', S S';
  sub [@upper @lower] s' lookup toCursive @lower;
  sub g.cursive s' lookup toCursive;
  sub [@upper @lower] @quotesingle s' lookup toCursive;
  sub S' lookup toCursive @lower;

  # t
  @notBeforet  = [@d @f @l];
  @beforet     = [@c @p @tCursive @sCursive @SCursive];
  @notAftert   = [@h @k @l @upper];
  @aftert      = [@r @s @w];

  ignore sub     @notBeforet  t'                                            ;
  ignore sub                  t'                    @notAftert              ;
  sub            @beforet     t' lookup toCursive                           ;
  sub                         t' lookup toCursive                  @aftert  ;
  sub                         t' lookup toCursive     @quotesingle @aftert  ;
  sub                         t' lookup toCursive   t              @aftert  ;
  sub                         t' lookup toCursive   t @quotesingle @aftert  ;         ;
}} cursiveAlts;

###############################################################################
# Sprawling glyphs (Takes up extra space but doesn't change width)            #
###############################################################################

lookup toSprawl {{
  sub A                    by  A.sprawl.s           ;
  sub B                    by  B.sprawl.nw          ;
  sub C                    by  C.sprawl.s           ;
  sub D                    by  D.sprawl.nw          ;
  sub f                    by  f.sprawl.sw          ;
  sub i                    by  i.sprawl.w           ;
  sub J                    by  J.sprawl.s           ;
  sub j                    by  j.sprawl.s           ;
  sub K                    by  K.sprawl.se          ;
  sub k                    by  k.sprawl.se          ;
  sub L                    by  L.sprawl.s           ;
  sub l                    by  l.sprawl.w           ;
  sub N                    by  N.sprawl.s           ;
  sub P                    by  P.sprawl.nw          ;
  sub Q                    by  Q.sprawl.se          ;
  sub q                    by  q.sprawl.se          ;
  sub R                    by  R.sprawl.se          ;
  sub t.cursive            by  t.cursive.sprawl.e   ;
  sub V                    by  V.sprawl.nwne        ;
  sub X                    by  X.sprawl.s           ;
  sub Y                    by  Y.sprawl.nwne        ;
  sub Z                    by  Z.sprawl.se          ;
  sub z                    by  z.sprawl.se          ;
}} toSprawl;

lookup toSprawlAlt {{
  sub C                    by  C.sprawl.e           ;
  sub F                    by  F.sprawl.e           ;
  sub R                    by  R.sprawl.nw          ;
  sub R.sprawl.se          by  R.sprawl.nwse        ;
  sub s.cursive            by  s.cursive.sprawl.w   ;
  sub V                    by  V.sprawl.w           ;
  sub Y                    by  Y.sprawl.w           ;
  sub Z                    by  Z.sprawl.s           ;
  sub z                    by  z.sprawl.s           ;
}} toSprawlAlt;

@blocksFirstCapSprawl = [@upper @liningDigits];
lookup sprawl1 {{
  ignore sub @blocksFirstCapSprawl  [A C J L N X Z]'                          ;
  ignore sub @lower                 [J j z]'                                  ;
  ignore sub @blocksSprawlSW        f'                                        ;
  ignore sub @blocksSprawlNWSwash   [B D P]'                                  ;
  ignore sub @blocksSprawlNW        [V Y]'                                    ;
  ignore sub                        [V Y]'           @blocksSprawlNE          ;

  @CCompat = [@xHeight @d @q];
  @FCompat = [@A @CCompat @lowerNotTall];
  sub C' lookup toSprawlAlt @CCompat;
  sub F' lookup toSprawlAlt @FCompat;
  sub Z' lookup toSprawlAlt @blocksSprawlSE.upper;
  sub z' lookup toSprawlAlt @blocksSprawlSE.lower;

  sub [@F @P @T @r @v @quotesingle] s.cursive' lookup toSprawlAlt;

  ignore sub                   [K Q R]'              @blocksSprawlSE.upper    ;
  ignore sub                   [k q]'                @blocksSprawlSE.lower    ;
  ignore sub                   t.cursive'            @blocksSprawlE.tCursive  ;

  sub [A B C D f J j K k L N P Q q R t.cursive V X Y Z z]' lookup toSprawl;
}} sprawl1;

lookup sprawl2 {{
  ignore sub @blocksSprawlNWSwash @R';
  sub [R R.sprawl.se]' lookup toSprawlAlt;
  sub [{t('L', '!sprawl')}] [V Y]' lookup toSprawlAlt;
}} sprawl2;

###############################################################################
# Thin-Wide Pairings                                                          #
###############################################################################

lookup tw1 {{
  # Use ligatures for these double-letters so they are widened or thinned
  # together. Otherwise, the end result looks wrong. These glyphs are all
  # placeholders only used within this section.

  sub i i  by  ii;
  sub l l  by  ll;
  sub m m  by  mm;
  sub r r  by  rr;
  sub t t  by  tt;
  sub w w  by  ww;
}} tw1;

@wideUpperA = [ A      A.sprawl.s      G      M      S.cursive      W      ];
@wideUpperB = [ A.wide A.sprawl.s.wide G.wide M.wide S.cursive.wide W.wide ];
@wideLowerA = [ m      mm      w      ww      ];
@wideLowerB = [ m.wide mm.wide w.wide ww.wide ];
@narrowA = [ i      ii      j      j.sprawl.s l      ll      rr      tt      ];
@narrowB = [ i.thin ii.thin j.thin j.thin     l.thin ll.thin rr.thin tt.thin ];

lookup widen {{
  sub [@wideUpperA @wideLowerA] by [@wideUpperB @wideLowerB];
}} widen;

lookup narrow {{
  sub [
    @narrowA
    L L.sprawl.s
    quotesingle
    i.midthin l.midthin
  ] by [
    @narrowB
    L.thin.sprawl.se L.thin.sprawl.se
    quotesingle.thin
    i.thin l.thin
  ];
}} narrow;

lookup narrowJ {{
  sub [J J.sprawl.s j] by [J.thin.sprawl.sw J.thin.sprawl.sw j.thin.sprawl.sw];
}} narrowJ;

lookup tw2 {{
  # Find pairs of letters to thin and wide

  ignore sub @upper @wideUpperA';

  @Lt = [L L.sprawl.s];
  @jt = [J J.sprawl.s j];

  # Sub immediate pairs.
  # Wj
  sub
    [@wideUpperA @wideLowerA]' lookup widen
    @jt' lookup narrowJ;
  # Wi
  sub
    [@wideUpperA @wideLowerA]' lookup widen
    @narrowA' lookup narrow;
  # W'x
  sub
    [@wideUpperA @wideLowerA]' lookup widen
    quotesingle' lookup narrow
    [@upper @lower];
  # xjw
  sub
    @lowerNotDescending
    @jt' lookup narrowJ
    @wideLowerA' lookup widen;
  # iw / Lw
  sub
    [@narrowA @Lt]' lookup narrow
    @wideLowerA' lookup widen;
  # X'w
  sub
    [@upper @lower]
    quotesingle' lookup narrow
    @wideLowerA' lookup widen;
  
  # With space in the middle
  @skip = [{t('lower', '!width')}];
  @skipBeforeJ = [{t('lower', '!descending', '!accentUnder', '!width')} @p thorn];
  @skipAfterL = [{t('lower', '!descending', '!accentUnder', '!width')} @q];
{''.join(f"""
  # W{'x' * i}j
  sub
    [@wideUpperA @wideLowerA]' lookup widen
    {'@skip ' * (i - 1)} @skipBeforeJ
    @jt' lookup narrowJ;
  # Wxi
  sub
    [@wideUpperA @wideLowerA]' lookup widen
    {'@skip ' * i}
    @narrowA' lookup narrow;
  # W{'x' * i}'x
  sub
    [@wideUpperA @wideLowerA]' lookup widen
    {'@skip ' * i}
    quotesingle' lookup narrow
    [@upper @lower];
  # xj{'x' * i}w
  sub
    [@lowerNotDescending @p thorn]
    @jt' lookup narrowJ
    {'@skip ' * i}
    @wideLowerA' lookup widen;
  # i{'x' * i}w
  sub
    @narrowA' lookup narrow
    {'@skip ' * i}
    @wideLowerA' lookup widen;
  # x'{'x' * i}w
  sub
    [@upper @lower]
    quotesingle' lookup narrow
    {'@skip ' * i}
    @wideLowerA' lookup widen;
  # L{'x' * i}w
  sub
    @Lt' lookup narrow
    @skipAfterL {'@skip ' * (i - 1)}
    @wideLowerA' lookup widen;
""" for i in range(1, 3))}
}} tw2;

lookup midden {{
  sub [
    i i.thin
    l l.thin
    r
    t
    m m.wide
    w w.wide
  ] by [
    i.midthin i.midthin
    l.midthin l.midthin
    r.midthin
    t.midthin
    m.midwide m.midwide
    w.midwide w.midwide
  ];
}} midden;

lookup tw3 {{
  # Balance pairs of nearby letters

{''.join(f"""
  # i{'x' * i}i
  sub
   [i l r t]' lookup midden
   {'@lower ' * i}
   [i.thin l.thin]' lookup midden;
  sub
   [i.thin l.thin]' lookup midden
   {'@lower ' * i}
   [i l r t]' lookup midden;
  # w{'x' * i}w
  sub
   [m w]' lookup midden
   {'@lower ' * i}
   [m.wide w.wide]' lookup midden;
  sub
   [m.wide w.wide]' lookup midden
   {'@lower ' * i}
   [m w]' lookup midden;
""" for i in range(0, 3))}
}} tw3;

lookup tw4 {{
  # Remove double-letter ligatures

  sub ii       by  i         i;
  sub ll       by  l         l;
  sub mm       by  m         m;
  sub rr       by  r         r;
  sub tt       by  t         t;
  sub ww       by  w         w;
  sub ii.thin  by  i.midthin i.midthin;
  sub ll.thin  by  l.midthin l.midthin;
  sub rr.thin  by  r.midthin r.midthin;
  sub tt.thin  by  t.midthin t.midthin;
  sub mm.wide  by  m.midwide m.midwide;
  sub ww.wide  by  w.midwide w.midwide;
}} tw4;

lookup proportional1 {{
  # Primary proportional glyph subs

  sub A                by  A.proportional;
  sub A.sprawl.s       by  A.proportional;
  sub A.wide           by  A.proportional;
  sub A.sprawl.s.wide  by  A.proportional;
  sub C.sprawl.e       by  C.sprawl.e.proportional;
  sub D                by  D.proportional;
  sub G                by  G.proportional;
  sub H                by  H.proportional;
  sub I                by  I.midthin;
  sub i                by  i.thin;
  sub i.midthin        by  i.thin;
  sub L                by  L.proportional;
  sub l                by  l.thin;
  sub l.midthin        by  l.thin;
  sub M                by  M.wide;
  sub m                by  m.wide;
  sub m.midwide        by  m.wide;
  sub N                by  N.proportional;
  sub r                by  r.midthin;
  sub S.cursive        by  S.cursive.wide;
  sub t                by  t.midthin;
  sub V                by  V.proportional;
  sub V.sprawl.nwne    by  V.proportional;
  sub W                by  W.wide;
  sub w                by  w.wide;

  sub space            by  space.proportional;
  sub emdash           by  emdash.proportional;

  sub quotesingle      by  quotesingle.thin;
  sub period           by  period.proportional;
  sub comma            by  comma.proportional;
  sub semicolon        by  semicolon.proportional;
  sub colon            by  colon.proportional;
}} proportional1;

lookup proportional2 {{
  # Perform any contextual substitutions

  sub L.sprawl.s' [@lowerNotDescending @q] by L.thin.sprawl.se;
}} proportional2;

lookup proportionalPos {{
  pos [A.proportional L.sprawl.s L.proportional] [{t('Y', 'sprawl')}] -30;
  pos [T quotesingle.thin] [@lowerNotTall @lowerRightTall] -100;
  pos [@L @lowerNotTall @lowerLeftTall] [T V.proportional {t('Y', '!sprawl')} @f longs quotesingle.thin]  -100;
  pos V.proportional [@lowerNotTall @lowerRightTall A.proportional] -30;
  pos [@lowerNotTall @lowerLeftTall] V.proportional -30;
}} proportionalPos;

###############################################################################
# Final Cleanup & Ligatures                                                   #
###############################################################################

@wantSprawlW.il = [
  L L.sprawl.s i.sprawl.w l.sprawl.w
];

lookup sprawl3 {{
  # If we get here with unmodified "i" or "l" glyphs, attempt to balance them
  # visually based on their position in the word.
  # This is an incredibly minor tweak, but helps to hide defects in certain
  # words like "application" and "api"

  ignore sub                                  [i l]'                  j                ;
  sub                        @wantSprawlW.il  [i l]' lookup toSprawl                   ;
  ignore sub                               i  i'                                       ;
  ignore sub                               l  l'                                       ;
  ignore sub                                  i'                      [@lower]         ;
  sub         [@lowerNotTall @lowerLeftTall]  [i l]' lookup toSprawl                   ;
}} sprawl3;

lookup flourish {{
  sub @flourishCompatSW [f f.sprawl.sw y]' by [f.flourish.sw f.flourish.sw y.flourish.sw];
}} flourish;

lookup cursiveJoiners {{
  sub  @tCursive' @tCursive        by  t.cursive.before.t;
  sub  @tCursive' [i.thin l.thin]  by  t.cursive.before.i.thin;
}} cursiveJoiners;

lookup cursiveLigatures {{
  sub  b          s.cursive  by  bs.cursive;

  sub  g.cursive  r          by  gr.cursive;
  sub  g.cursive  s.cursive  by  gs.cursive;

  sub  i          s.cursive  by  is.cursive;
  sub  i.sprawl.w s.cursive  by  is.sprawl.w.cursive;
  sub  i.midthin  s.cursive  by  is.cursive.midthin;
  sub  i.thin     s.cursive  by  is.cursive.thin;

  sub  l          s.cursive  by  ls.cursive;
  sub  l.sprawl.w s.cursive  by  ls.sprawl.w.cursive;
  sub  l.midthin  s.cursive  by  ls.cursive.midthin;
  sub  l.thin     s.cursive  by  ls.cursive.thin;

  sub o           s.cursive  by  os.cursive;

  sub  t.cursive  r          by  tr.cursive;
  sub  t.cursive  r.midthin  by  tr.cursive.midthin;
  sub  t.cursive  s.cursive  by  ts.cursive;

  sub t.cursive quotesingle.thin s.cursive by tquotesingles.cursive.thin;
}} cursiveLigatures;

###############################################################################
# Feature Definitions (order here doesn't actually matter)                    #
###############################################################################

feature calt {{
  script DFLT;
    language dflt ;
    lookup sprawl1;
    lookup sprawl2;
    lookup sprawl3;
    lookup tw1;
    lookup tw2;
    lookup tw3;
    lookup tw4;
  script latn;
    language dflt ;
    lookup sprawl1;
    lookup sprawl2;
    lookup sprawl3;
    lookup tw1;
    lookup tw2;
    lookup tw3;
    lookup tw4;
}} calt;

feature lnum {{
  script DFLT;
    language dflt ;
    lookup lining;
  script latn;
    language dflt ;
    lookup lining;
}} lnum;

feature ss01 {{
  script DFLT;
    language dflt ;
    lookup cursiveAlts;
  script latn;
    language dflt ;
    lookup cursiveAlts;
}} ss01;

feature ss02 {{
  script DFLT;
    language dflt ;
    lookup cursiveJoiners;
    lookup cursiveLigatures;
  script latn;
    language dflt ;
    lookup cursiveJoiners;
    lookup cursiveLigatures;
}} ss02;

feature ss03 {{
  script DFLT;
    language dflt ;
    lookup flourish;
  script latn;
    language dflt ;
    lookup flourish;
}} ss03;

feature ss08 {{
  script DFLT;
    language dflt ;
    lookup proportional1;
    lookup proportional2;
    lookup proportionalPos;
  script latn;
    language dflt ;
    lookup proportional1;
    lookup proportional2;
    lookup proportionalPos;
}} ss08;

feature ss16 {{
  script DFLT;
    language dflt ;
    lookup hexify;
    lookup afterHexify;
  script latn;
    language dflt ;
    lookup hexify;
    lookup afterHexify;
}} ss16;
"""

if __name__ == '__main__':
    target_directory = 'cantrip.sfdir'
    all_glyphs = get_glyphs(target_directory)
    tagged_glyphs = tag_glyphs(all_glyphs)
    with open("features/generated.fea", "w") as f:
      f.write(get_defs(tagged_glyphs))