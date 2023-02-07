from MatchingTools import match_devices


def adapter(combos, links):
    """
    combos: Dictionary mapping combo name to list of names of active links
    links: list of link names
    """

    # construct cluster center tokens
    linkname2linkidx = {}
    for i, l in enumerate(links):
        linkname2linkidx[l] = i
    
    cluster_centers = [] # when populated, should have the same length as combos
    for _, active_links in combos.items():
        active_idxs = [linkname2linkidx[l] for l in active_links]
        # construct token from active_idxs. Token should be the same length as links
        center_token = tuple(1 if i in active_idxs else 0 for i in range(len(links)))
        cluster_centers.append(center_token)

    return cluster_centers


def test_matching(centers, links):
    match_devices(centers, links) # prints out results
    
def main():
    # Run tests here
    combos = {
        "Combo1": ['4C72700E0D.4C72700E1C', '4C72700E1C.4C72700E0D', '4C72700E1C.4C72700E2C', '4C72700E1C.f081731d0c40', '4C72700E2C.4C72700E1C'],
        "Combo2": ['4C72700E2C.4C72700E2E', '4C72700E2E.4C72700E2C'],
        "Combo3": ['4C72700E0D.4C72700E1C', '4C72700E1C.4C72700E0D'],
        "Combo4": ['4C72700E1C.4C72700E2C', '4C72700E2C.4C72700E1C', '4C72700E2C.4C72700E2E', '4C72700E2C.58d34926c760', '4C72700E2E.4C72700E2C'],
        "Combo5": ['4C72700E2C.4C72700E2E', '4C72700E2C.58d34926c760', '4C72700E2E.4C72700E2C'],
        "Combo6": ['4C72700E0D.4C72700E1C', '4C72700E1C.4C72700E0D', '4C72700E1C.f081731d0c40'],
        "Combo7": ['4C72700E2C.58d34926c760'],
        "Combo8": ['4C72700E0D.4C72700E1C', '4C72700E1C.4C72700E0D', '4C72700E1C.4C72700E2C', '4C72700E2C.4C72700E1C'],
        "Combo9": ['4C72700E1C.f081731d0c40', '4C72700E2C.4C72700E2E', '4C72700E2E.4C72700E2C'],
        "Combo10": ['4C72700E0D.4C72700E1C', '4C72700E1C.4C72700E0D', '4C72700E1C.4C72700E2C', '4C72700E1C.f081731d0c40'],
            }
    links = ['4C72700E0D.4C72700E1C',
            '4C72700E1C.4C72700E0D',
            '4C72700E1C.4C72700E2C',
            '4C72700E1C.f081731d0c40',
            '4C72700E2C.4C72700E1C',
            '4C72700E2C.4C72700E2E',
            '4C72700E2C.58d34926c760',
            '4C72700E2E.4C72700E2C']

    centers = adapter(combos, links)
    test_matching(centers, links)

if __name__=="__main__":
    main()
