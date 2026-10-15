from __future__ import annotations
import NXOpen
# import NXOpen.UF

class Session:

    @staticmethod    
    def work_part() -> NXOpen.Part :
        return NXOpen.Session.GetSession().Parts.Work
    
    @staticmethod
    def uf_session() -> NXOpen.UF.UFSession:
        import NXOpen.UF
        return NXOpen.UF.UFSession.GetUFSession()