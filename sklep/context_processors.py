def koszyk(request): return {'stan_koszyka':len(request.session.get('koszyk', []))}
#def klient(request): return {'klient':len(request.session.get('klient', []))}