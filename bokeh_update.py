from ipykernel.comm import Comm
from IPython import display
import bokeh

update_bokeh_comm = None

def install_javascript():
    display.display_html('<script src="bokeh_update.js"></script>', raw=True)
    global update_bokeh_comm
    update_bokeh_comm = Comm(target_name='bokeh_update_target',
                             target_module='bokeh_update', data={})


def replace_bokeh_data_source(ds):
    update_bokeh_comm.send({"custom_type": "replace_bokeh_data_source",
            "ds_id": ds.ref['id'], # Model Id
            "ds_model": ds.ref['type'], # Collection Type
            "ds_json": bokeh.protocol.serialize_json(ds.vm_serialize())
    })

