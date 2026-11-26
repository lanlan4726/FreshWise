"""Public FreshWise demo. Visitor-owned Gemini key; original Python decision tools."""
import base64
import json
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src' if (ROOT / 'src').is_dir() else ROOT.parent / 'src'
sys.path.insert(0, str(SOURCE))
ASSETS = ROOT / 'assets' if (ROOT / 'assets').is_dir() else ROOT.parent / 'assets'
import streamlit as st
from cloud_context import demo_context, snapshot
from freshwise.application_tools import invoke

st.set_page_config(page_title='FreshWise | Public demo', page_icon='🌿', layout='wide')
page = st.sidebar.radio('Explore FreshWise', ['Prep plan', 'AI assistant', 'Impact'])
st.sidebar.caption('Historical demo · Centre 13 · Week 146. Not a current-week forecast.')
if page == 'AI assistant':
    runpy.run_path(str(ROOT / 'agent_lan_demo.py'), run_name='__main__')
    st.stop()

st.html('''<style>
.stApp{background:#faf8f2;color:#203e32}
[data-testid="stMainBlockContainer"]{max-width:1100px;padding-top:2rem}
[data-testid="stSidebar"]{background:#f0f2e8}
.brand{display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #dde3d6;padding-bottom:20px;margin-bottom:25px}
.brand .project{width:245px;max-width:65%}.brand .team{width:85px}
.ticket{background:#fff;border:1px solid #dce3d5;border-top:5px solid #32634a;border-radius:18px;padding:24px;margin:18px 0}
.ticket h2{font-size:38px;color:#203e32;margin:5px 0 14px}.ticket p{font-size:17px}
.credit{border-top:1px solid #dde3d6;padding-top:16px;margin-top:25px;font-size:14px;color:#64715e}
</style>''')
def encoded(name):
    return base64.b64encode((ASSETS/name).read_bytes()).decode()
st.html(f'<div class="brand"><img class="project" alt="FreshWise" src="data:image/png;base64,{encoded("freshwise-logo.png")}"><img class="team" alt="SALLAS" src="data:image/png;base64,{encoded("sallas-logo.png")}"></div>')
st.caption('Public planning prototype. No real kitchen action is sent. Forecast snapshots are historical; this site does not retrain a model.')

if page == 'Prep plan':
    st.title('What should you prepare?')
    st.write('Use your ready portions first. Review a new preparation plan using the original FreshWise decision tools.')
    meal = st.selectbox('Dish at centre 13', [1198,2306,2444,2664], format_func=lambda m:f'Meal {m}')
    context = demo_context(13, meal)
    st.caption(f'Historical planning week {context.forecast_record["target_week"]} · Expected orders about {context.forecast:.2f}')
    with st.form('manual_plan'):
        stock = st.number_input('How many portions do you already have ready to use?', min_value=0,value=20,step=1)
        adjust = st.checkbox('Include a manager estimate')
        estimate = st.number_input('Estimated orders for this dish',min_value=0,value=600,step=1)
        weight = st.selectbox('How far should we move toward your estimate?', ['Small change (25%)','Meet halfway (50%)','Use my estimate (100%)'])
        preview = st.form_submit_button('Preview preparation plan',type='primary')
    identity = (meal,stock,adjust,estimate,weight)
    old = st.session_state.get('manual_preview')
    if old and old['identity'] != identity:
        st.session_state.pop('manual_preview',None)
    active = st.session_state.get('manual_active')
    if active and active['meal'] != meal:
        st.session_state.pop('manual_active',None)
        active = None
    if preview:
        central = invoke('central_preparation_recommendation', {'usable_stock':stock},context=context)
        result = central
        plan = central['result']
        if adjust:
            result = invoke('manager_adjusted_central_recommendation',
                {'usable_stock':stock,'manager_estimate':estimate,'opinion_weight':{'Small change (25%)':.25,'Meet halfway (50%)':.5,'Use my estimate (100%)':1}[weight]},context=context)
            plan = result['result']['adjusted_plan']
        st.session_state['manual_preview']={'identity':identity,'meal':meal,'plan':plan,'output':result,'original':central['result']}
    pending = st.session_state.get('manual_preview')
    if active:
        st.success(f'Confirmed demo plan: prepare {active["plan"]["new_portions_to_prepare"]} NEW portions; use {active["plan"]["usable_stock"]} ready portions first.')
    if pending:
        plan = pending['plan']
        st.html(f'<div class="ticket"><p>PREVIEW · NOT APPLIED</p><h2>Prepare {plan["new_portions_to_prepare"]} new portions</h2><p>Use {plan["usable_stock"]} ready portions first.</p></div>')
        if adjust:
            st.write(f'Original → adjusted: **{pending["original"]["new_portions_to_prepare"]} → {plan["new_portions_to_prepare"]}** new portions.')
        if st.button('Confirm and apply demo plan',type='primary'):
            st.session_state['manual_active']=pending
            st.session_state.pop('manual_preview',None)
            st.rerun()
        if st.button('Discard preview'):
            st.session_state.pop('manual_preview',None)
            st.rerun()
        with st.expander('Exact tool trace'):
            st.json(pending['output'])
    with st.expander('Forecast snapshot and assumptions'):
        st.write('These four forecast snapshots were generated with the project forecasting tools from historical data. No CSV files are required on the hosting server. Quantities are recalculated by the original Python decision functions for each input.')
        st.json(context.forecast_record)
elif page == 'Impact':
    st.title('Waste and service trade-offs')
    st.write('Team-reported historical simulation on weeks 136–145. These results do not predict waste for a new plan.')
    group=st.radio('Simulation group',['Four demo meals','All meals'],horizontal=True)
    rows = {'Four demo meals':[(16.6,1.5),(18.8,7.2)],'All meals':[(17.9,2.2),(16.7,20.6)]}[group]
    a,b=st.columns(2)
    a.metric('Simulated waste incl. terminal stock',f'{rows[0][1]}%',f'{rows[0][1]-rows[0][0]:+.1f} percentage points',delta_color='inverse')
    b.metric('Unmet observed orders',f'{rows[1][1]}%',f'{rows[1][1]-rows[1][0]:+.1f} percentage points',delta_color='inverse')
    st.write(f'Baseline → default waste: **{rows[0][0]}% → {rows[0][1]}%**. Unmet orders: **{rows[1][0]}% → {rows[1][1]}%**.')
    if group=='All meals':
        st.warning('Across all meals, the default reduces simulated waste but worsens service. It does not meet the no-worse-service floor.')
    st.caption('Baseline: last-week forecast without carry-over. Default: HGB forecast minus usable stock; zero starting stock; oldest usable stock first; one extra week of shelf life as a simulation assumption. Waste includes expired portions and usable terminal stock. Source: final-run results reported by Silvia in the team update, not independently re-evaluated here.')
    st.info('Recipe-based ingredient sharing, food safety verification, real stock tracking and carbon-savings calculations are outside this prototype.')

st.html('<div class="credit">Lan · Conversation interface, Gemini integration, application adapter and public demo<br>Silvia · Forecasting model and forecast tools<br>Ari · Preparation policy and decision tools<br>FreshWise by SALLAS · Historical demonstration, not operational advice</div>')
