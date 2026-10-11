import * as cg from 'chessgroundx/types';
import * as util from 'chessgroundx/util';

import { _ } from './i18n';
import type { Variant } from './variants';

// Names keyed by piece letter ('r', '+p'); pieceName() translates them when shown,
// since these tables are built before the translations load.
export type PieceNameTable = Readonly<Record<string, string>>;

const CHESS: PieceNameTable = {
    k: _('king'),
    q: _('queen'),
    r: _('rook'),
    b: _('bishop'),
    n: _('knight'),
    p: _('pawn'),
};

const XIANGQI: PieceNameTable = {
    k: _('king'),
    a: _('advisor'),
    b: _('elephant'),
    n: _('horse'),
    r: _('chariot'),
    c: _('cannon'),
    p: _('pawn'),
};

// Piece families whose k, q, r, b, n, p are the chess pieces (checked against their rules pages).
const FAMILY_TABLES: Readonly<Record<string, PieceNameTable>> = {
    standard: CHESS,
    capa: CHESS,
    seirawan: CHESS,
    shogun: CHESS,
    orda: CHESS,
    xiangqi: XIANGQI,
    janggi: XIANGQI,
};

/** A piece's full name, from the variant's own table, then its family's, else its letter. */
export function pieceName(variant: Variant, role: cg.Role, color: cg.Color): string {
    const letter = util.letterOf(role);
    const name =
        variant.pieceNamesByColor?.[color]?.[letter] ??
        variant.pieceNames?.[letter] ??
        FAMILY_TABLES[variant.pieceFamily]?.[letter];
    return name === undefined ? letter : _(name);
}
