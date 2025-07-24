from bokeh.models import CDSView, GroupFilter, CheckboxGroup, ColorBar, CustomJS, Slider, Dropdown, Select, Button, LinearColorMapper, AutocompleteInput, Div, Label, LabelSet, CheckboxGroup, HoverTool, LassoSelectTool, ColumnDataSource
from bokeh.layouts import layout, row, column
from bokeh.models.widgets import DataTable, TableColumn, HTMLTemplateFormatter
from bokeh.plotting import figure, show, curdoc
from bokeh.events import Reset
from pathlib import Path
import pandas as pd
import sqlite3
import re
from . import data_load
from .data_load import dataset_LDA2D, color, df_mesh, colors_mesh, product_names

source = ColumnDataSource(data=dict(LDA1=dataset_LDA2D.LDA1, 
                                         LDA2=dataset_LDA2D.LDA2,
                                         colors=color,
                                         class_colors=color,
                                         map_value=dataset_LDA2D.predictions_label,
                                         Taxon_IDs=dataset_LDA2D.Taxon_ID,
                                         Analysis_Project_IDs=dataset_LDA2D.AP_ID,
                                         GOLD_IDs=dataset_LDA2D.GOLD,
                                         GOLD_Ecosystem=dataset_LDA2D.GOLD_Ecosystem,
                                         GOLD_Category=dataset_LDA2D.GOLD_Category,
                                         GOLD_Type=dataset_LDA2D.GOLD_Type,
                                         GOLD_Subtype=dataset_LDA2D.GOLD_Subtype,
                                         GOLD_Specific=dataset_LDA2D.GOLD_Specific,
                                         map_classification=dataset_LDA2D.predictions_label))

button_source = ColumnDataSource(data=dict(LDA1=dataset_LDA2D.LDA1, 
                                         LDA2=dataset_LDA2D.LDA2,
                                         colors=color,
                                         class_colors=color,
                                         map_value=dataset_LDA2D.predictions_label,
                                         Taxon_IDs=dataset_LDA2D.Taxon_ID,
                                         Analysis_Project_IDs=dataset_LDA2D.AP_ID,
                                         GOLD_IDs=dataset_LDA2D.GOLD,
                                         GOLD_Ecosystem=dataset_LDA2D.GOLD_Ecosystem,
                                         GOLD_Category=dataset_LDA2D.GOLD_Category,
                                         GOLD_Type=dataset_LDA2D.GOLD_Type,
                                         GOLD_Subtype=dataset_LDA2D.GOLD_Subtype,
                                         GOLD_Specific=dataset_LDA2D.GOLD_Specific,
                                         map_classification=dataset_LDA2D.predictions_label))

source_mesh = ColumnDataSource(data=dict(x=df_mesh.xx.to_numpy(),
                                         y=df_mesh.yy.to_numpy(),
                                         pred=df_mesh.pred.to_numpy(),
                                         colors_mesh=colors_mesh))

lasso_source = ColumnDataSource(data=dict(LDA1=[],
											LDA2=[],
											Taxon_IDs=[],
											colors=[],
											GOLD_Subtype=[],
											GOLD_Specific=[],
											map_value=[]))

"""
Plot
"""
# Initiate Plot
tools_ = ['crosshair', 'zoom_in', 'zoom_out', 'save', 'reset', 'tap', 'box_zoom', 'pan', 'undo', 'redo', 'wheel_zoom', 'help']
p = figure(title="Metagenome Tetranucleotide Linear Discriminant Analysis Dimensionality Reduction and k-Nearest Neighbors Ecosystem Classification", 
	tools=tools_, toolbar_location="left", y_axis_location="right", active_drag="box_zoom", width=1750, height=1500)

# axis labels
p.xaxis.axis_label = 'LDA1'
p.yaxis.axis_label = 'LDA2'

a_deep = CDSView(filter=GroupFilter(column_name="map_classification", group="Aquatic>Deep subsurface"))
freshwater = CDSView(filter=GroupFilter(column_name="map_classification", group="Aquatic>Freshwater"))
marine = CDSView(filter=GroupFilter(column_name="map_classification", group="Aquatic>Marine"))
saline = CDSView(filter=GroupFilter(column_name="map_classification", group="Aquatic>Non-marine Saline and Alkaline"))
thermal = CDSView(filter=GroupFilter(column_name="map_classification", group="Aquatic>Thermal springs"))
soil = CDSView(filter=GroupFilter(column_name="map_classification", group="Terrestrial>Soil"))

# plots
p_a_deep = p.scatter('LDA1', 'LDA2', fill_color='colors',
              size=7, alpha=0.5, line_alpha=0,
              source=source, view=a_deep, name='a_deep', legend_group='GOLD_Type')
p_freshwater = p.scatter('LDA1', 'LDA2', fill_color='colors',
              size=7, alpha=0.5, line_alpha=0,
              source=source, view=freshwater, name='freshwater', legend_group='GOLD_Type')
p_marine = p.scatter('LDA1', 'LDA2', fill_color='colors',
              size=7, alpha=0.5, line_alpha=0,
              source=source, view=marine, name='marine', legend_group='GOLD_Type')
p_saline = p.scatter('LDA1', 'LDA2', fill_color='colors',
              size=7, alpha=0.5, line_alpha=0,
              source=source, view=saline, name='saline', legend_group='GOLD_Type')
p_thermal = p.scatter('LDA1', 'LDA2', fill_color='colors',
              size=7, alpha=0.5, line_alpha=0,
              source=source, view=thermal, name='thermal', legend_group='GOLD_Type')
p_soil = p.scatter('LDA1', 'LDA2', fill_color='colors',
              size=7, alpha=0.5, line_alpha=0,
              source=source, view=soil, name='soil', legend_group='GOLD_Type')
p_map = p.scatter(x='x', y='y', marker='square', fill_color='colors_mesh',
              size=8, line_alpha=0, fill_alpha=0.15,
              source=source_mesh, name='Mesh')#, legend_group='pred')
p.x_range.range_padding = 0
p.y_range.range_padding = 0
p.xgrid.visible = False
p.ygrid.visible = False
p.legend.title="GOLD Ecosystem Type"
p.legend.location = 'top_left'
p.legend.orientation="vertical"
p.legend.background_fill_alpha = 0
#p.legend.click_policy="hide"
p.title.text_font_size = '14pt'
p.add_layout(p.legend[0], 'right')

# add hovertool
hover_1 = HoverTool(tooltips=[("IMG Taxon ID", "@Taxon_IDs"), ("IMG AP ID", "@Analysis_Project_IDs"), ("GOLD Analysis ID", "@GOLD_IDs"), ("GOLD Ecosystem", "@GOLD_Ecosystem"), ("GOLD Category", "@GOLD_Category"), ("GOLD Type", "@GOLD_Type"), ("GOLD Subtype", "@GOLD_Subtype"), ("GOLD Specific", "@GOLD_Specific"), ("Mapped Value", "@map_value"), (" ",' ')],
	renderers=[p_freshwater,p_marine,p_saline,p_thermal,p_soil])
p.add_tools(hover_1)
lasso_1 = LassoSelectTool(continuous=False)
p.add_tools(lasso_1)

column_width=540

guide_link = Div(text="""<a target="_blank" rel="noopener noreferrer" href="https://microbiomes.jgi.doe.gov/myapp/static/UI_Guide.pdf">User Interface Guide</a>""", styles={'font-size': '150%', 'color': 'blue'})

button_note = Div(text="<div>NOTE: With Safari, Download button will open the data in a new tab, rather than start a download.</div>", width=column_width)
button = Button(label="Download All", button_type="danger")
button.js_on_event("button_click",CustomJS(
        args=dict(source=button_source),
        code=(Path(__file__).parent / "download.js").read_text("utf8"),
    ),
)

autocomp_title = Div(text="<div><strong>Protein Annotation View</strong> (Mapped Value = counts per 1 billion assembled bases;</div><div>Metagenomes with no abundance are hidden)</div><div>Examples: COG0001, KO:K00001, PF00001, EC:1.1.1.1</div><div>'Ecosystem' to reset.</div><div>Enter a protein annotation ID and move the heat color scale slider to try it out.</div>", width=column_width)
autocomp = AutocompleteInput(title="", completions=product_names, case_sensitive=False)
heat_slider = Slider(start=1, end=11, value=6, step=1, title="Protein Annotation View Heat Color Scale")

table_title = Div(text="<div><strong>Selection Table:</strong></div>", width=column_width)
lasso_table = DataTable(source=lasso_source, columns=[TableColumn(field='Taxon_IDs', title="Selected Taxon IDs", formatter=HTMLTemplateFormatter(template='<a href="https://img.jgi.doe.gov/cgi-bin/mer/main.cgi?section=TaxonDetail&page=taxonDetail&taxon_oid=<%= Taxon_IDs %>" target="_blank"><%= value %></a>'), width=110),TableColumn(field='GOLD_Subtype', title="GOLD Subtype", width=140),TableColumn(field='GOLD_Specific', title="GOLD Specific", width=140),TableColumn(field='map_value', title="Mapped Value", width=150)], height=1050)
lasso_callback = CustomJS(args=dict(lasso_source=lasso_source, source=source, lasso_table=lasso_table, button=button, button_source=button_source), code="""
    var inds = cb_obj.indices;
    var s1 = source.data;
    var ld = lasso_source.data;
    ld['Taxon_IDs'] = [];
    ld['LDA1'] = [];
    ld['LDA2'] = [];
    ld['colors'] = [];
    ld['GOLD_Subtype'] = [];
    ld['GOLD_Specific'] = [];
    ld['map_value'] = [];
    for (var i = 0; i < inds.length; i++) {
        ld['Taxon_IDs'].push(s1['Taxon_IDs'][inds[i]]);
        ld['LDA1'].push(s1['LDA1'][inds[i]]);
        ld['LDA2'].push(s1['LDA2'][inds[i]]);
        ld['colors'].push(s1['class_colors'][inds[i]]);
        ld['GOLD_Subtype'].push(s1['GOLD_Subtype'][inds[i]]);
        ld['GOLD_Specific'].push(s1['GOLD_Specific'][inds[i]]);
        ld['map_value'].push(s1['map_value'][inds[i]]);
    }
    lasso_source.change.emit();
    lasso_table.change.emit();
    var bd = button_source.data;
    bd['Taxon_IDs'] = [];
    bd['LDA1']=[];
	bd['LDA2']=[];
	bd['colors']=[];
	bd['class_colors']=[];
	bd['map_value']=[];
	bd['Analysis_Project_IDs']=[];
	bd['GOLD_IDs']=[];
	bd['GOLD_Ecosystem']=[];
	bd['GOLD_Category']=[];
	bd['GOLD_Type']=[];
	bd['GOLD_Subtype']=[];
	bd['GOLD_Specific']=[];
	bd['map_classification']=[];
    for (var i = 0; i < inds.length; i++) {
		bd['Taxon_IDs'].push(s1['Taxon_IDs'][inds[i]]);
		bd['LDA1'].push(s1['LDA1'][inds[i]]);
		bd['LDA2'].push(s1['LDA2'][inds[i]]);
		bd['colors'].push(s1['class_colors'][inds[i]]);
		bd['class_colors'].push(s1['class_colors'][inds[i]]);
		bd['map_value'].push(s1['map_value'][inds[i]]);
		bd['Analysis_Project_IDs'].push(s1['Analysis_Project_IDs'][inds[i]]);
		bd['GOLD_IDs'].push(s1['GOLD_IDs'][inds[i]]);
		bd['GOLD_Ecosystem'].push(s1['GOLD_Ecosystem'][inds[i]]);
		bd['GOLD_Category'].push(s1['GOLD_Category'][inds[i]]);
		bd['GOLD_Type'].push(s1['GOLD_Type'][inds[i]]);
		bd['GOLD_Subtype'].push(s1['GOLD_Subtype'][inds[i]]);
		bd['GOLD_Specific'].push(s1['GOLD_Specific'][inds[i]]);
		bd['map_classification'].push(s1['map_classification'][inds[i]]);
    }
    button_source.change.emit();
    button.label="Download Selection";
""")

source.selected.js_on_change('indices', lasso_callback)

reset_callback = CustomJS(args=dict(button=button, source=source, button_source=button_source), code="""
    var bd = button_source.data;
    var s1 = source.data;
    bd['Taxon_IDs']=s1['Taxon_IDs'];
    bd['LDA1']=s1['LDA1'];
	bd['LDA2']=s1['LDA2'];
	bd['colors']=s1['colors'];
	bd['class_colors']=s1['class_colors'];
	bd['map_value']=s1['map_value'];
	bd['Analysis_Project_IDs']=s1['Analysis_Project_IDs'];
	bd['GOLD_IDs']=s1['GOLD_IDs'];
	bd['GOLD_Ecosystem']=s1['GOLD_Ecosystem'];
	bd['GOLD_Category']=s1['GOLD_Category'];
	bd['GOLD_Type']=s1['GOLD_Type'];
	bd['GOLD_Subtype']=s1['GOLD_Subtype'];
	bd['GOLD_Specific']=s1['GOLD_Specific'];
	bd['map_classification']=s1['map_classification'];
    button_source.change.emit();
    button.label="Download All";
""")

p.js_on_event(Reset, reset_callback)

p.x_range.js_on_change('start', reset_callback)
p.x_range.js_on_change('end', reset_callback)

def marker_callback(attr, old, new):
	sel_inds = source.selected.indices
	source.selected.indices = []
	if(autocomp.value == "Ecosystem"):
		p.legend.visible = True
		source.data['colors'] = color
		source.data['map_value'] = dataset_LDA2D.predictions_label
		source.selected.indices = sel_inds
	else:
		p.legend.visible = False
		directory="null"
		product=autocomp.value
		product_file=product.replace(":","_")
		product_file=product_file.replace(".","_")
		product_file=product_file.replace("-","_")
		if re.match(r'^COG',product):
			directory="COG"
		elif re.match(r'^EC',product):
			directory="EC"
		elif re.match(r'^KO',product):
			directory="KO"
		elif re.match(r'^PF',product):
			directory="PFAM"
		path = '/myapp/data/'+directory+'/'+product_file+'.db'
		con = sqlite3.connect(path)
		query = 'SELECT * FROM '+product_file
		product_df = pd.read_sql_query(query, con)
		con.close()
		values = [ '%.1f' % elem for elem in product_df.product_values.to_list() ]
		source.data['map_value'] = [float(x) for x in values]
		button_source.data['map_value'] = source.data['map_value']
		if(heat_slider.value == 1):
			source.data['colors'] = product_df.product_sources0_001.to_list()
		elif(heat_slider.value == 2):
			source.data['colors'] = product_df.product_sources0_01.to_list()
		elif(heat_slider.value == 3):
			source.data['colors'] = product_df.product_sources0_05.to_list()
		elif(heat_slider.value == 4):
			source.data['colors'] = product_df.product_sources0_1.to_list()
		elif(heat_slider.value == 5):
			source.data['colors'] = product_df.product_sources0_25.to_list()
		elif(heat_slider.value == 6):
			source.data['colors'] = product_df.product_sources0_5.to_list()
		elif(heat_slider.value == 7):
			source.data['colors'] = product_df.product_sources.to_list()
		elif(heat_slider.value == 8):
			source.data['colors'] = product_df.product_sources10.to_list()
		elif(heat_slider.value == 9):
			source.data['colors'] = product_df.product_sources50.to_list()
		elif(heat_slider.value == 10):
			source.data['colors'] = product_df.product_sources100.to_list()
		elif(heat_slider.value == 11):
			source.data['colors'] = product_df.product_sources500.to_list()
		source.selected.indices = sel_inds
	
heat_slider.on_change('value', marker_callback)
autocomp.on_change('value', marker_callback)

def update_points(attr, old, new):
	p_a_deep.visible = 0 in checkbox_group.active
	p_freshwater.visible = 1 in checkbox_group.active
	p_marine.visible = 2 in checkbox_group.active
	p_saline.visible = 3 in checkbox_group.active
	p_thermal.visible = 4 in checkbox_group.active
	p_soil.visible = 5 in checkbox_group.active
    
checkbox_group = CheckboxGroup(labels=["Aquatic>Deep subsurface (Purple)", "Aquatic>Freshwater (Blue)", "Aquatic>Marine (Green)", "Aquatic>Non-marine Saline and Alkaline (Pink)", "Aquatic>Thermal springs (Gold)", "Terrestrial>Soil (Red)"], active=[0,1,2,3,4,5])
checkbox_group.on_change("active", update_points)
checkbox_text = Div(text="<div><strong>Plotted KNN Metagenome Ecosystem Classifications:</strong></div>")

line1 = Div(text="_____________________________________")
line2 = Div(text="_____________________________________")

annotation_column = column(autocomp_title,row(autocomp,heat_slider),line1,checkbox_text,checkbox_group,line2,table_title,button,button_note,lasso_table)

collapse = Button(label="Collapse Annotation Panel", button_type="danger")

reference = Div(text="""Reference: <a target="_blank" rel="noopener noreferrer" href="https://journals.asm.org/doi/10.1128/msystems.01744-24">Kellom, M., et al. 2025. \"Tetranucleotide frequencies differentiate genomic boundaries and metabolic strategies across environmental microbiomes.\" <i>mSystems</i> 0:e01744-24. doi: 10.1128/msystems.01744-24</a>""")

status = Div(text="""This page runs on the Spin platform and displays data hosted on the Community File System (CFS) of NERSC. Check their status and maintenance schedules: <a target="_blank" rel="noopener noreferrer" href="https://www.nersc.gov/users/status">Here</a>""")

#note = Div(text="""NOTE: IMG will be undergoing database upgrades July 8 - July 21. Any links to IMG pages may not be functional during this time.</a>""", styles={'font-size': '200%', 'color': 'red'})

def collapse_button():
	global layout, collapse
	curdoc().hold("combine")
	if collapse.label=="Collapse Annotation Panel":
		collapse.label="Expand Annotation Panel"
		new_layout = row(p)
	elif collapse.label=="Expand Annotation Panel":
		collapse.label="Collapse Annotation Panel"
		new_layout = row(annotation_column,p)
	layout.children[2] = new_layout #with no note
	#layout.children[3] = new_layout #with note
	curdoc().unhold()

collapse.on_click(collapse_button)

img_button = Button(label="IMG HOME")
img_callback = CustomJS(code='''window.open('https://img.jgi.doe.gov/', '_blank').focus();''')
img_button.js_on_click(img_callback)

initial = row(annotation_column,p)
layout = column(guide_link,row(collapse,img_button),initial,reference,status) #with no note
#layout = column(note,guide_link,row(collapse,img_button),initial,reference,status) #with note
layout.name = "app"
curdoc().add_root(layout)
curdoc().title = "IMG Metagenomes 4mer LDA and KNN Model"