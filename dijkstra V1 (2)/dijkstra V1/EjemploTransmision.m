%Sistema Información 
%Diseño óptimo de ruta para linea de transmisión
%UTP-InterColombia

clc;
clear all;

%Micro área
h=1; %alto km
w=1; %ancho km

%Tamaño de la zona en áreas
H=100; %alto km
W=100; %ancho km

%OJO: H y h deben ser multiplos    Igualmente H y h

%Costos/km para el peor escenario Bosque tipo 1 ;  pendiente tipo 1
%Sobre este costo operan los factores
CostoBosque=   1000000; %US$/km
CostoPendiente=100000; %US$/km
CostoDistancia=100000;  %US$/km
CostoVias=400000;
%Zonas activas: Corresponde a demarcar la región de interés
filename='mapasv1.xlsx';
ZonasActivas='MicroAreas Activas';
Zacti = xlsread(filename,ZonasActivas);
ZonasBosque='Bosque';
Zbosq = xlsread(filename,ZonasBosque);
ZonasPendiente='Pendiente';
Zpend = xlsread(filename,ZonasPendiente);

ZonasVias='Vias';
Zvias = xlsread(filename,ZonasVias);

% Zacti=[0	0	0	3	1	1	0	0	1	1
% 1	0	0	1	1	1	0	0	1	1
% 1	1	1	1	1	1	1	1	1	1
% 1	0	0	0	0	0	0	0	0	1
% 1	0	0	0	0	0	0	0	0	1
% 1	0	0	0	0	0	0	0	0	1
% 1	1	1	1	1	1	1	1	1	1
% 0	0	0	0	0	0	1	1	1	0
% 0	0	0	0	0	0	1	1	0	0
% 2	1	1	1	1	1	1	0	0	0
% ];  %OJO: La MicroArea Inicial =2  MicroAreaFinal=3

%Zona Boscosa 1=tipo 1 (alto)   2= Tipo 2 (medio)  3=Tipo 3 (bajo)
% Zbosq=[0	0	0	1	1	1	0	0	1	3
% 1	0	0	3	1	1	0	0	2	3
% 3	1	2	3	1	1	1	1	1	1
% 3	0	0	0	0	0	0	0	0	1
% 3	0	0	0	0	0	0	0	0	1
% 3	0	0	0	0	0	0	0	0	1
% 3	3	3	3	3	3	2	1	1	1
% 0	0	0	0	0	0	1	1	1	0
% 0	0	0	0	0	0	1	2	0	0
% 3	1	3	2	3	1	2	0	0	0
% ];
 
 FCost_Zbosq=[1 0.5 0]; %Factores que operan sobre el costo peor escenario
 FCost_Zvia=[0 0.5 0.8 2 4];
 
 %Pendiente de la zona   3 tipos de pendiente (1 (alta), 2 (media), 3
 %(baja)
%  Zpend=[0	0	0	2	3	1	0	0	1	3
% 2	0	0	2	1	1	0	0	1	3
% 1	1	2	1	1	2	3	2	3	3
% 2	0	0	0	0	0	0	0	0	2
% 1	0	0	0	0	0	0	0	0	1
% 1	0	0	0	0	0	0	0	0	1
% 2	1	3	3	2	1	3	3	3	1
% 0	0	0	0	0	0	2	3	1	0
% 0	0	0	0	0	0	1	3	0	0
% 2	1	3	2	3	1	1	0	0	0
% ];

  FCost_Zpend=[1 0.3 0.2];  %Factores que operan sobre el costo peor escenario 
  
  
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 %Calculo Matriz adyascencias Ady
 
 [rows,cols]=find(Zacti); %Encontrar indices de las áreas activas <> 0

 pos=find(Zacti); %Encontrar Posiciones lineales de las áreas activas
 NumMicroAreas=size(pos,1);
 NumColumnas=W/w;
 NumFilas=H/h;
 
 %          [nuevo ind , pos original, ind fila, ind columna]
 MapaMicroAreaActiva=[[1:NumMicroAreas]',pos, rows,cols]; 
 
 MicroAreaIni=find(Zacti==2);  %MicroArea donde Inicia el proyecto
 MicroAreaFin=find(Zacti==3);  %MicroArea donde Termina el proyecto
 
 PuntoIni=find(MapaMicroAreaActiva(:,2)==MicroAreaIni);
 PuntoFin=find(MapaMicroAreaActiva(:,2)==MicroAreaFin);
 
 
 %Toda micro-área X puede tener 8 vecinos  [1] [2] [3]
                                       %   [4]  X  [5]
                                       %   [6] [7] [8]
 
  %%%% Construción del mapa que relaciona cada micro-área con sus vecinos
  %%%% activos
  MapaVecinosMicroAreas=zeros(NumMicroAreas, 8);  
  MapaVecinoDiagonales=zeros(NumMicroAreas, 8);
  for i=1:NumMicroAreas
      X=MapaMicroAreaActiva(i,2);    %Pos original de micro-area 
      
      ConsiderarLimitesAbajo=false; %Considerar no evaluar vecinos por fuera de los limites
      ConsiderarLimitesArriba=false;
      if MapaMicroAreaActiva(i,3)==NumFilas  
          ConsiderarLimitesAbajo=true;
      end
      if MapaMicroAreaActiva(i,3)==1  
          ConsiderarLimitesArriba=true;
      end      
          
      %Obtener las posiciones (nuevo ind) de los 8 vecinos ACTIVOS
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
                      if (m==1 & n==1) | (m==1 & n==3) | (m==3 & n==1) | (m==3 & n==3) %Si se trata de un vecino Diagonal
                          MapaVecinoDiagonales(i,contador)=1;    %1= diagonal
                      elseif (m==1 & n==2) | (m==3 & n==2) %Si es vecino horizontal
                          MapaVecinoDiagonales(i,contador)=2;    %2= horizontal
                      else  %Si es vecino Vertical
                          MapaVecinoDiagonales(i,contador)=3;    %3= vertical
                      end                                                                
                      MapaVecinosMicroAreas(i,contador)=PosVecino;
                  end
              end
          end
      end
  end
  
%%%% Construcción de la matriz de ponderaciones
AdyPonderaciones=zeros(NumMicroAreas,NumMicroAreas); %Matriz de distancias ponderadas de unicamente las micro-áreas activas  
for MicroArea=1:NumMicroAreas %para cada micro-area
    for v=1:8  %para cada vecino
        Vecino=MapaVecinosMicroAreas(MicroArea,v);
        if Vecino==0  %Rompe el for si no hay más vecinos
            break
        end
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %   C A L C U L O  D E  L O S  D I F E R E N T E S   F A C T O R E S
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %Distancia %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        if MapaVecinoDiagonales(MicroArea,v)==1  %si se trata de un vecino diagonal
            FDistancia=sqrt(h^2+w^2);
        elseif MapaVecinoDiagonales(MicroArea,v)==2 %Si es vecino horizontal
            FDistancia=w;  %ancho
        elseif MapaVecinoDiagonales(MicroArea,v)==3 %Si es vecino verticalmente
            FDistancia=h;  %altura
        end
        CostoTramoDistancia=CostoDistancia*FDistancia;
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %Bosque %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        TipoBosqueMicroArea_i= Zbosq(MapaMicroAreaActiva(MicroArea, 2)); %Tipo bosque microarea i
        if TipoBosqueMicroArea_i==0
            Fbosque_i=0;
        else
            Fbosque_i=FCost_Zbosq(TipoBosqueMicroArea_i);
        end
        TipoBosqueMicroArea_j= Zbosq(MapaMicroAreaActiva(Vecino   , 2)); %Tipo bosque vecino j
        if TipoBosqueMicroArea_j==0
            Fbosque_j=0;
        else
            Fbosque_j=FCost_Zbosq(TipoBosqueMicroArea_j);
        end
        CostoTramoBosque=(Fbosque_i+Fbosque_j)*FDistancia/2*CostoBosque;
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %Cercanía a Vias  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        TipoViaMicroArea_i= Zvias(MapaMicroAreaActiva(MicroArea, 2)); %Tipo via microarea i
        if TipoViaMicroArea_i==0
            Fvia_i=0;
        else
            Fvia_i=FCost_Zvia(TipoViaMicroArea_i);
        end
        TipoViaMicroArea_j= Zvias(MapaMicroAreaActiva(Vecino   , 2)); %Tipo bosque vecino j
        if TipoViaMicroArea_j==0
            Fvia_j=0;
        else
            Fvia_j=FCost_Zvia(TipoViaMicroArea_j);
        end
        CostoTramoVia=(Fvia_i+Fvia_j)*FDistancia/2*CostoVias;
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %Pendiente %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        TipoPendMicroArea_i= Zpend(MapaMicroAreaActiva(MicroArea, 2)); %Tipo bosque microarea i
        if TipoPendMicroArea_i==0
            Fpend_i=0;
        else
            Fpend_i=FCost_Zpend(TipoPendMicroArea_i);
        end
        TipoPendMicroArea_j= Zpend(MapaMicroAreaActiva(Vecino   , 2)); %Tipo bosque vecino j
        if TipoPendMicroArea_j==0
            Fpend_j=0;
        else
            Fpend_j=FCost_Zpend(TipoPendMicroArea_j);
        end
        CostoTramoPendiente=(Fpend_i+Fpend_j)*FDistancia/2*CostoPendiente;
        
        %%%%%%%   AQUÍ SE ADJUNTAN TODOS LOS FACTORES A CONSIDERAR
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        AdyPonderaciones(MicroArea, Vecino)=CostoTramoDistancia +...
                                            CostoTramoBosque    +...
                                            CostoTramoPendiente +...
                                            CostoTramoVia;
        
    end
end
[e L] = dijkstra(AdyPonderaciones,PuntoIni,PuntoFin)

MatSol=zeros(NumFilas,NumColumnas);
for i=1:size(L,2)
    Pos=L(i);
    fila=MapaMicroAreaActiva(Pos,3);
    columna=MapaMicroAreaActiva(Pos,4);
    MatSol(fila,columna)=1;
end
    
      
                                     
                                     
  
