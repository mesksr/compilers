
%%
"if"                      printf("<IF>\n");
"then"                    printf("<THEN>\n");
"else"                    printf("<ELSE>\n");
[_a-zA-Z][_a-zA-Z0-9]*    printf("<VARIABLE>\n");
(>|>=|<|<=|==|!=)         printf("<REL OP>\n");
"="                       printf("<ASSIGN OP>\n");
" "
%%

int yywrap(void)
{
	return 1;
}
