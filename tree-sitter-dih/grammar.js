module.exports = grammar({
  name: 'dih',

  extras: $ => [/[ \t]+/],

  rules: {
    source_file: $ => seq(
      repeat(seq($._line, '\n')),
      optional($._line),
    ),

    _line: $ => choice(
      $.norm_line,
      prec(-1, $.arrow_line),
    ),

    arrow_line: $ => seq(
      $.arrow,
      optional($.in_name),
      $.node_name,
    ),
    
    norm_line: $ => seq(
      optional($.in_name),
      optional($.node_name),
      optional($.nice),
      $.op,
      optional($.trail)
    ),
    
    arrow: $ => choice("->", "<-"),
    in_name: $ => seq("(", $._in_name_inner, ")"),
    node_name: $ => seq("[", $._node_name_inner, "]"),
    nice: $ => seq("{", $.number, "}"),
    op: $ => token(prec(-1, /[^\/\r\n]+/)),

    trail: $ => seq(
      "/",
      optional($.number),
      ",",
      optional($.number),
      ",",
      optional($.trailtrail)
    ),
    
    trailtrail: $ => seq(
      commaSep1($.trail_inner),
      optional(","),
    ),

    number: $ => /\d+/,
    _in_name_inner: $ => /[^)\r\n]*/,
    _node_name_inner: $ => /[^\]\r\n]*/,
    trail_inner: $ => /[^,\r\n]*/,
  }
})

function commaSep1(rule) {
  return sep1(rule, ',');
}

function sep1(rule, separator) {
  return seq(rule, repeat(seq(separator, rule)));
}
