

clc;
clear all;

h=1; 
w=1; 

H=100; 
W=100; 

CostoBosque=   1000000; 
CostoPendiente=100000; 
CostoDistancia=100000;  
CostoVias=400000;

filename='mapaini.xlsx';
ZonasActivas='acti';
Zacti = xlsread(filename,ZonasActivas);
ZonasBosque='bosq';
Zbosq = xlsread(filename,ZonasBosque);
ZonasPendiente='pend';
Zpend = xlsread(filename,ZonasPendiente);

ZonasVias='vias';
Zvias = xlsread(filename,ZonasVias);

FCost_Zbosq=[1 0.5 0]; 
FCost_Zvia=[0 0.5 0.8 2 4];
FCost_Zpend=[1 0.3 0.2];  
[rows,cols]=find(Zacti); 
pos=find(Zacti); 
NumMicroAreas=size(pos,1);
NumColumnas=W/w;
NumFilas=H/h;

MapaMicroAreaActiva=[[1:NumMicroAreas]',pos, rows,cols]; 

MicroAreaIni=find(Zacti==2);  
MicroAreaFin=find(Zacti==3);  

PuntoIni=find(MapaMicroAreaActiva(:,2)==MicroAreaIni);
PuntoFin=find(MapaMicroAreaActiva(:,2)==MicroAreaFin);
                                 
MapaVecinosMicroAreas=zeros(NumMicroAreas, 8);  
MapaVecinoDiagonales=zeros(NumMicroAreas, 8);
for i=1:NumMicroAreas
    X=MapaMicroAreaActiva(i,2);    
      
    ConsiderarLimitesAbajo=false; 
    ConsiderarLimitesArriba=false;
    if MapaMicroAreaActiva(i,3)==NumFilas  
        ConsiderarLimitesAbajo=true;
    end
    if MapaMicroAreaActiva(i,3)==1  
        ConsiderarLimitesArriba=true;
    end      
          
      
    contador=0;  
    cont_i=-1;
    Lim_m=3;
    Lim_n=3;
    for m=1:Lim_m
        if ConsiderarLimitesArriba
            Vecino=X+cont_i*NumFilas; 
            Lim_n=2;
        else
          Vecino=X+cont_i*NumFilas-1;  
        end
        cont_i=cont_i+1;
        cont_j=0;
        if ConsiderarLimitesAbajo
            Lim_n=2;
        end
        for n=1:Lim_n                  
            Vecino=Vecino+cont_j;
            cont_j=1;
            if Vecino~=X;                                                
                PosVecino=find(MapaMicroAreaActiva(:,2)==Vecino);
                if size(PosVecino,1)~=0
                    contador=contador+1;
                    if (m==1 & n==1) | (m==1 & n==3) | (m==3 & n==1) | (m==3 & n==3) 
                        MapaVecinoDiagonales(i,contador)=1;    
                    elseif (m==1 & n==2) | (m==3 & n==2) 
                        MapaVecinoDiagonales(i,contador)=2;    
                    else  
                        MapaVecinoDiagonales(i,contador)=3;    
                    end                                                                
                    MapaVecinosMicroAreas(i,contador)=PosVecino;
                end
            end
        end
    end
end

AdyPonderaciones=zeros(NumMicroAreas,NumMicroAreas); 
for MicroArea=1:NumMicroAreas 
    for v=1:8  
        Vecino=MapaVecinosMicroAreas(MicroArea,v);
        if Vecino==0  
            break
        end
        
        
        
        
        
        
        if MapaVecinoDiagonales(MicroArea,v)==1  
            FDistancia=sqrt(h^2+w^2);
        elseif MapaVecinoDiagonales(MicroArea,v)==2 
            FDistancia=w;  
        elseif MapaVecinoDiagonales(MicroArea,v)==3 
            FDistancia=h;  
        end
        CostoTramoDistancia=CostoDistancia*FDistancia;
        
        
        
        TipoBosqueMicroArea_i= Zbosq(MapaMicroAreaActiva(MicroArea, 2)); 
        if TipoBosqueMicroArea_i==0
            Fbosque_i=0;
        else
            Fbosque_i=FCost_Zbosq(TipoBosqueMicroArea_i);
        end
        TipoBosqueMicroArea_j= Zbosq(MapaMicroAreaActiva(Vecino   , 2)); 
        if TipoBosqueMicroArea_j==0
            Fbosque_j=0;
        else
            Fbosque_j=FCost_Zbosq(TipoBosqueMicroArea_j);
        end
        CostoTramoBosque=(Fbosque_i+Fbosque_j)*FDistancia/2*CostoBosque;
        
        
        TipoViaMicroArea_i= Zvias(MapaMicroAreaActiva(MicroArea, 2)); 
        if TipoViaMicroArea_i==0
            Fvia_i=0;
        else
            Fvia_i=FCost_Zvia(TipoViaMicroArea_i);
        end
        TipoViaMicroArea_j= Zvias(MapaMicroAreaActiva(Vecino   , 2)); 
        if TipoViaMicroArea_j==0
            Fvia_j=0;
        else
            Fvia_j=FCost_Zvia(TipoViaMicroArea_j);
        end
        CostoTramoVia=(Fvia_i+Fvia_j)*FDistancia/2*CostoVias;
        
        
        
        TipoPendMicroArea_i= Zpend(MapaMicroAreaActiva(MicroArea, 2)); 
        if TipoPendMicroArea_i==0
            Fpend_i=0;
        else
            Fpend_i=FCost_Zpend(TipoPendMicroArea_i);
        end
        TipoPendMicroArea_j= Zpend(MapaMicroAreaActiva(Vecino   , 2)); 
        if TipoPendMicroArea_j==0
            Fpend_j=0;
        else
            Fpend_j=FCost_Zpend(TipoPendMicroArea_j);
        end
        CostoTramoPendiente=(Fpend_i+Fpend_j)*FDistancia/2*CostoPendiente;
        
        
        
        
        
        AdyPonderaciones(MicroArea, Vecino)=CostoTramoDistancia +...
                                            CostoTramoBosque    +...
                                            CostoTramoPendiente +...
                                            CostoTramoVia;
        
    end
end
[e L] = dijkstra(AdyPonderaciones,PuntoIni,PuntoFin);

MatSol=zeros(NumFilas,NumColumnas);
for i=1:size(L,2)
    Pos=L(i);
    fila=MapaMicroAreaActiva(Pos,3);
    columna=MapaMicroAreaActiva(Pos,4);
    MatSol(fila,columna)=1;
end
    
      
                                     
                                     
  
