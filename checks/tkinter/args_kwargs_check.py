def xesta(*args, **kwargs):
    print(args, args==(), len(args))
    a,b,c=args
    print(kwargs)
    print(kwargs.get('aba'))
    print()
ppp=xesta
xesta(a='sdfsdf', qwere=123333)
ppp(aba='23234')
xesta(123,555,ggg=12)