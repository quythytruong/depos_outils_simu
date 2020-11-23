import pandas as pd
def histogramme_duree_h(df_suivi = pd.DataFrame):
    ax = df_suivi.hist(column='duree_estimee_h',
                                            bins=50,
                                            grid=False,
                                            figsize=(8,10), 
                                            layout=(3,1), 
                                            sharex=True, 
                                            color='#86bf91', 
                                            zorder=2, 
                                            rwidth=0.9)

    ax = ax[0]
    for x in ax:
        # Despine
        x.spines['right'].set_visible(False)
        x.spines['top'].set_visible(False)
        x.spines['left'].set_visible(False)
        
        # Switch off ticks
        x.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")
            
            
        # Draw horizontal axis lines
        vals = x.get_yticks()
        for tick in vals:
            x.axhline(y=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)
        
        # Remove title
        x.set_title("")
    
        # Set x-axis label
        x.set_xlabel("Durée estimée (heures)", labelpad=20, weight='bold', size=12)
        
        # Set y-axis label
        x.set_ylabel("Nombre de trajets", labelpad=20, weight='bold', size=12)
        
def histogramme_variation_duree(durees = pd.DataFrame, column_name = str):
    ax = durees.hist(column= column_name, 
                   bins=50, 
                   grid=False, 
                   figsize=(8,10), 
                   layout=(3,1), 
                   sharex=True, 
                   color='#86bf91', 
                   zorder=2, 
                   rwidth=0.9)
    ax = ax[0]
    for x in ax:
            
        # Despine
        x.spines['right'].set_visible(False)
        x.spines['top'].set_visible(False)
        x.spines['left'].set_visible(False)
        
        # Switch off ticks
        x.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")
        
                
        # Draw horizontal axis lines
        vals = x.get_yticks()
        for tick in vals:
            x.axhline(y=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)
        
        # Remove title
        x.set_title("")
        
        # Set x-axis label
        x.set_xlabel("Variation de durée (h)", labelpad=20, weight='bold', size=12)
        
        # Set y-axis label
        x.set_ylabel("Nombre de trajets", labelpad=20, weight='bold', size=12)
        
def histogramme(dataset = pd.DataFrame, column_name = str, 
                xlabel = str, ylabel = str):
    ax = dataset.hist(column= column_name, 
                   bins=50, 
                   grid=False, 
                   figsize=(8,10), 
                   layout=(3,1), 
                   sharex=True, 
                   color='#86bf91', 
                   zorder=2, 
                   rwidth=0.9)
    ax = ax[0]
    for x in ax:
            
        # Despine
        x.spines['right'].set_visible(False)
        x.spines['top'].set_visible(False)
        x.spines['left'].set_visible(False)
        
        # Switch off ticks
        x.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")
        
                
        # Draw horizontal axis lines
        vals = x.get_yticks()
        for tick in vals:
            x.axhline(y=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)
        
        # Remove title
        x.set_title("")
        
        # Set x-axis label
        x.set_xlabel(xlabel, labelpad=20, weight='bold', size=12)
        
        # Set y-axis label
        x.set_ylabel(ylabel, labelpad=20, weight='bold', size=12)
    return ax

def vol_dechets_AD(data_AD = pd.DataFrame, column_name = str):
    titre_abscisse = "Volume de déchets (m3)"
    titre_ordonnee = "Nombre d'aires de dépose"
    histogramme(data_AD, column_name, titre_abscisse, titre_ordonnee)
    
def distance_bati_AD(data_AD = pd.DataFrame, column_name = str):
    titre_abscisse = "Distance à l'aire de dépose la plus proche (m)"
    titre_ordonnee = "Nombre de bâtiments"
    histogramme(data_AD, column_name, titre_abscisse, titre_ordonnee)