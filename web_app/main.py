import streamlit as st
from streamlit.report_thread import get_report_ctx
from streamlit.hashing import _CodeHasher
from streamlit.server.server import Server

from old_bill_app import old_bill_search
from new_bill_app import new_bill_search

'''
# How Will They Vote?

Please choose an option from the sidebar
'''

def main():
    pages = {
        "New Bills": new_bill_page,
        "Old Bills": old_bill_page,
    }

    st.sidebar.title("Bill type")
    page = st.sidebar.radio("Select your page", list(pages.keys()))

    pages[page](_get_state())


def new_bill_page(state):
    st.markdown('# New Bill Voting')

    st.markdown('This is specific to the 116th Congress')
    st.markdown('Please enter your bill information in the sidebar')

    new_bill_search()


def old_bill_page(state):
    st.markdown('# Old Bill Voting')

    st.markdown('Comparing model against reality')
    st.markdown('Enter your information on the left.')
    st.markdown('Congress guide:')
    st.markdown('**116**: 2018 - 2020  \n\
                 **115**: 2016 - 2018  \n\
                 **114**: 2014 - 2016  \n\
                 **113**: 2012 - 2014')

    old_bill_search()


class _SessionState:

    def __init__(self, session):
        """Initialize SessionState instance."""
        # Attributes are initialized through __dict__ to avoid calling __setattr__.
        self.__dict__.update({
            "_code_hasher": _CodeHasher(),
            "_item_rerun": set(),
            "_session": session,
            "_state": {}
        })

    def __call__(self, **kwargs):
        """Initialize state data once."""
        for item, value in kwargs.items():
            if item not in self._state:
                self._state[item] = value

    def __getattr__(self, item):
        """Returns a saved state value, or None if undefined."""
        return self._state.get(item, None)
    
    def __getitem__(self, item):
        """Returns a saved state value, or None if undefined."""
        return self._state.get(item, None)
    
    def __setattr__(self, item, value):
        """Set state value. Request rerun if value changed.
        
        This is important to avoid keeping the old state value and get rollbacks. 
        Ensures to trigger a rerun once to avoid infinite loops (state.value += 1).
        """
        if item in self._item_rerun:
            self._item_rerun.remove(item)
        
        elif item not in self._state or self._normalize(self._state[item]) != self._normalize(value):
            self._item_rerun.add(item)
            self._session.request_rerun()

        self._state[item] = value
    
    def __setitem__(self, item, value):
        """Set state value."""
        return self.__setattr__(item, value)
    
    def _normalize(self, obj):
        """Normalize an object for comparison using Streamlit's converter to bytes."""
        return self._code_hasher.to_bytes(obj, None)
    
    def clear(self):
        """Clear session state and request a rerun."""
        self._state.clear()
        self._session.request_rerun()


def _get_session():
    ctx = get_report_ctx()
    session_id = ctx.session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")
    
    return session_info.session


def _get_state():
    session = _get_session()

    if not hasattr(session, "_custom_session_state"):
        session._custom_session_state = _SessionState(session)

    return session._custom_session_state


if __name__ == "__main__":
    main()