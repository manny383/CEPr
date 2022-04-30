from flask import Flask, render_template, request, flash, redirect, abort, url_for
from flask_bootstrap import Bootstrap
from modelo.DAO import db, Carreras, Grupo, Periodo, Usuarios, Alumnos, Docentes, Coordinador
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

app=Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://userControlEscolar:Hola.123@localhost/ControlEscolar'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='cl4v3'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'
login_manager.login_message = u"¡Debes de iniciar sesión!"



@login_manager.user_loader
def load_user(id):
    return Usuarios.query.get(int(id))

########################################################################################################################
#Sección LOGIN

@app.route('/')
def inicio():
    return render_template('Usuarios/Login.html')

@app.route('/cerrarSesion')
@login_required
def cerrarSesion():
        logout_user()
        return redirect(url_for('login'))

@app.route('/usuarios/ingresar')
def login():
    return render_template('Usuarios/Login.html')

@app.route('/usuarios/login' , methods=['post'])
def validarUsuario():
    user=Usuarios()
    email=request.form['email']
    contraseña=request.form['contraseña']
    user=user.validar(email,contraseña)
    if user!=None:
        login_user(user)
        return render_template('comunes/index.html')
    else:
        flash('¡Datos de la sesión incorrectos!')
        return render_template('Usuarios/Login.html')

#Fin
########################################################################################################################
########################################################################################################################
#Sección INDEX

@app.route('/index')
@login_required
def principal():
    if (current_user.is_authenticated):
        return render_template('comunes/index.html')
    else:
        abort(404)


#Fin
########################################################################################################################
########################################################################################################################
#Sección ALUMNOS



@app.route('/Alumnos/NuevoUsers')
@login_required
def AlumnosNuevoUsers():
    if (current_user.is_authenticated and (current_user.is_admin() or current_user.is_coordinador())):
        return render_template('Alumnos/NuevosUsers.html')
    else:
        abort(404)

@app.route('/Alumnos/Consulta')
@login_required
def AlumnosConsulta():
    if (current_user.is_authenticated and (current_user.is_admin() or current_user.is_coordinador())):
        a=Alumnos()
        alumnos=a.consultaGeneral()
        return render_template('Alumnos/Consulta.html', alumnos=alumnos)
    else:
        abort(404)


@app.route('/Alumnos/agregar', methods=['post'])
@login_required
def alumnosAgregar():
        a=Alumnos()
        a.idUsuario=request.form['usuario']
        a.idCarrera=request.form['carrera']
        a.anioIngreso=request.form['anioIngreso']
        a.insertar()
        flash('¡Registro Completo!')
        return redirect(url_for('AlumnosNuevoUsers'))


@app.route('/Alumnos/Nuevo')
@login_required
def AlumnosNuevo():
    if (current_user.is_authenticated and (current_user.is_admin() or current_user.is_coordinador())):
        u = Usuarios()
        c = Carreras()
        return render_template('Alumnos/Nuevo.html', usuarios=u.consultaGeneral(), carreras=c.consultaGeneral())
    else:
        abort(404)


@app.route('/Alumnos/ver/<int:id>')
@login_required
def consultarAlumno(id):
    if (current_user.is_authenticated and (current_user.is_admin() or current_user.is_coordinador())):
        a= Alumnos()
        c= Carreras()
        u= Usuarios()
        return render_template('/Alumnos/Modificar.html', alumnos=a.consultaIndividual(id),carreras=c.consultaGeneral(), usuarios=u.consultaIndividual(id))
    else:
        abort(404)

@app.route('/Alumnos/guardar' ,methods=['post'])
@login_required
def modificarAlumno():
    a=Alumnos()
    u=Usuarios()

    u.idUsuario= request.form['usuario']
    u.nombre = request.form['nombre']
    u.sexo = request.form['sexo']
    u.telefono = request.form['telefono']
    u.email = request.form['email']
    u.contraseña = request.form['contraseña']
    u.tipo = request.form['tipo']
    estatus= request.values.get('estatus', False)

    if estatus =="True":
        u.estatus=True
    else:
        u.estatus=False

    u.actualizar()


    a.noControl=request.form['noControl']
    a.idUsuario=request.form['usuario']
    a.idCarrera=request.form['carrera']
    a.anioIngreso=request.form['anioIngreso']
    a.actualizar()


    flash('¡Alumno actualizado con éxtio!')

    return redirect(url_for('AlumnosConsulta'))

@app.route('/Alumnos/eliminar/ <int:id>')
@login_required
def eliminarAlumnos(id):
    u=Usuarios()
    a=Alumnos()
    a.eliminar(id)
    u.eliminar(id)
    flash('¡Alumno eliminado con éxto!')
    return redirect(url_for('AlumnosConsulta'))


#Fin
########################################################################################################################
########################################################################################################################
#SECCIÓN DOCENTES

@app.route('/Docente/Consulta')
@login_required
def docentesConsulta():
    if (current_user.is_authenticated and (current_user.is_admin() or current_user.is_coordinador())):
        d=Docentes()
        docentes=d.consultaGeneral()
        return render_template('Docentes/Consulta.html', docentes=docentes)
    else:
        abort(404)

@app.route('/Docentes/NuevoUsers')
@login_required
def DocentesNuevoUsers():
    if (current_user.is_authenticated and (current_user.is_admin() or current_user.is_coordinador())):
        return render_template('Docentes/NuevosUsers.html')
    else:
        abort(404)

@app.route ('/Docentes/Nuevo')
@login_required
def docentesNuevo():
    if (current_user.is_authenticated and (current_user.is_admin() or current_user.is_coordinador())):
        u = Usuarios()
        c = Carreras()
        return render_template('Docentes/Nuevo.html', usuarios=u.consultaGeneral(), carreras=c.consultaGeneral())
    else:
        abort(404)

@app.route('/Docentes/agregar', methods=['post'])
@login_required
def docentesAgregar():
    d=Docentes()
    d.idUsuario=request.form['usuario']
    d.idCarrera=request.form['carrera']
    d.anioIngreso=request.form['anioIngreso']
    d.escolaridad=request.form['escolaridad']
    d.especialidad=request.form['especialidad']
    d.cedula=request.form['cedula']
    d.insertar()
    flash('¡Registro Completo!')
    return redirect(url_for('DocentesNuevoUsers'))

@app.route('/Docentes/ver/<int:id>')
@login_required
def consultarDocente(id):
    if (current_user.is_authenticated and current_user.is_admin()):
        d= Docentes()
        c= Carreras()
        u= Usuarios()
        return render_template('/Docentes/Modificar.html', docentes=d.consultaIndividual(id),carreras=c.consultaGeneral(), usuarios=u.consultaIndividual(id))
    else:
        abort(404)

@app.route('/Docentes/guardar' ,methods=['post'])
@login_required
def modificarDocente():
    d=Docentes()
    u=Usuarios()

    u.idUsuario= request.form['usuario']
    u.nombre = request.form['nombre']
    u.sexo = request.form['sexo']
    u.telefono = request.form['telefono']
    u.email = request.form['email']
    u.contraseña = request.form['contraseña']
    u.tipo = request.form['tipo']
    estatus= request.values.get('estatus', False)

    if estatus =="True":
        u.estatus=True
    else:
        u.estatus=False

    u.actualizar()


    d.noDocente=request.form['noDocente']
    d.idUsuario=request.form['usuario']
    d.idCarrera=request.form['carrera']
    d.anioIngreso=request.form['anioIngreso']
    d.escolaridad=request.form['escolaridad']
    d.especialidad= request.form['especialidad']
    d.cedula=request.form['cedula']
    d.actualizar()


    flash('¡Docente actualizado con éxtio!')

    return redirect(url_for('docentesConsulta'))

#Fin
########################################################################################################################
########################################################################################################################
#Sección Coordinador

@app.route('/Coordinador/NuevoUsers')
@login_required
def CoordinadorNuevoUsers():
    if(current_user.is_authenticated and current_user.is_admin()):
        return render_template('Coordinador/NuevosUsers.html')
    else:
        abort(404)

@app.route('/Coordinador/Consulta')
@login_required
def CoordinadorConsulta():
    if (current_user.is_authenticated and current_user.is_admin()):
        coor = Coordinador()
        coordinador = coor.consultaGeneral()
        return render_template('Coordinador/Consulta.html', coordinador=coordinador)
    else:
        abort(404)


@app.route ('/Coordinador/Nuevo')
@login_required
def coordinadorNuevo():
    if (current_user.is_authenticated and current_user.is_admin()):
        u = Usuarios()
        c = Carreras()
        return render_template('Coordinador/Nuevo.html', usuarios=u.consultaGeneral(), carreras=c.consultaGeneral())
    else:
        abort(404)

@app.route('/Coordinador/agregar', methods=['post'])
@login_required
def CoordinadorAgregar():
    co=Coordinador()
    co.idUsuario=request.form['usuario']
    co.idCarrera=request.form['carrera']
    co.fechaInicio=request.form['inicio']
    co.fechaFin=request.form['fin']
    co.insertar()
    flash('¡Registro Completo!')
    return redirect(url_for('CoordinadorNuevoUsers'))

@app.route('/Coordinador/ver/<int:id>')
@login_required
def consultarCoordinador(id):
    if (current_user.is_authenticated and current_user.is_admin()):
        co= Coordinador()
        c= Carreras()
        u= Usuarios()
        return render_template('/Coordinador/Modificar.html', coordinador=co.consultaIndividual(id),carreras=c.consultaGeneral(), usuarios=u.consultaIndividual(id))
    else:
        abort(404)


@app.route('/Coordinador/guardar' ,methods=['post'])
@login_required
def modificarCoordinador():
    co=Coordinador()
    u=Usuarios()

    u.idUsuario= request.form['usuario']
    u.nombre = request.form['nombre']
    u.sexo = request.form['sexo']
    u.telefono = request.form['telefono']
    u.email = request.form['email']
    u.contraseña = request.form['contraseña']
    u.tipo = request.form['tipo']
    estatus= request.values.get('estatus', False)

    if estatus =="True":
        u.estatus=True
    else:
        u.estatus=False

    u.actualizar()


    co.idCoordinador=request.form['idCoordinador']
    co.idUsuario=request.form['usuario']
    co.idCarrera=request.form['carrera']
    co.fechaInicio=request.form['inicio']
    co.fechaFin=request.form['fin']
    co.actualizar()


    flash('¡Docente actualizado con éxtio!')

    return redirect(url_for('CoordinadorConsulta'))

#Fin
########################################################################################################################
#SECCIÓN CARRERAS

@app.route('/Carreras')
@login_required
def carreras():
    if(current_user.is_authenticated and current_user.is_admin()):
        c=Carreras()
        carreras=c.consultaGeneral()
        return render_template('Carreras/Consulta.html', carreras=carreras)
    else:
        abort(404)


@app.route('/carreras/nuevo')
@login_required
def nuevaCarrera():
    if (current_user.is_authenticated and current_user.is_admin()):
        return render_template('Carreras/Nuevo.html')
    else:
        abort(404)


@app.route('/carreras/agregar', methods=['post'])
@login_required
def agregarCarrera():
    c=Carreras()
    c.nombre=request.form['nombre']
    c.siglas=request.form['siglas']
    c.especialidad=request.form['especialidad']
    c.creditos=request.form['creditos']
    c.insertar()
    flash('¡Carrera registrada con éxito!')
    return render_template('Carreras/Nuevo.html')

@app.route('/carreras/ver/<int:id>')
@login_required
def consultarCarreras(id):
    if (current_user.is_authenticated and current_user.is_admin()):
        c=Carreras()
        return render_template('Carreras/Modificar.html', carreras=c.consultaIndividual(id))
    else:
        abort(404)

@app.route('/carreras/guardar', methods=['post'])
@login_required
def modificarCarreras():
    c=Carreras()
    c.idCarrera = request.form['id']
    c.nombre = request.form['nombre']
    c.siglas = request.form['siglas']
    c.especialidad = request.form['especialidad']
    c.creditos = request.form['creditos']
    c.actualizar()
    flash('¡Carrera editada con éxito!')
    return redirect(url_for('carreras'))

@app.route('/carreras/eliminar/<int:id>')
@login_required
def eliminarCarreras(id):
    c=Carreras()
    c.eliminar(id)
    flash('¡Carrera eliminada con éxito!')
    return redirect(url_for('carreras'))

#Fin
########################################################################################################################


########################################################################################################################
#Sección GRUPOS

@app.route('/Grupos')
@login_required
def grupos():
    if (current_user.is_authenticated and (current_user.is_admin() or current_user.is_coordinador())):
        g=Grupo()
        grupos=g.consultaGeneral()
        return render_template('Grupo/Consulta.html', grupos=grupos)
    else:
        abort(404)



@app.route('/grupos/nuevo')
@login_required
def nuevoGrupo():
    if (current_user.is_authenticated and (current_user.is_admin() or current_user.is_coordinador())):
        p = Periodo()
        c = Carreras()
        return render_template('Grupo/Nuevo.html', periodo=p.consultaGeneral(),carreras=c.consultaGeneral())
    else:
        abort(404)

@app.route('/grupos/agregar', methods=['post'])
@login_required
def agregarGrupo():
    g=Grupo()
    g.idPeriodo=request.form['periodo']
    g.idCarrera=request.form['carrera']
    g.descripcion=request.form['descripcion']
    g.semestre=request.form['semestre']
    g.grupo=request.form['grupo']
    g.insertar()
    flash('¡Grupo registrado con éxito!')
    return render_template('/Grupo/Nuevo.html')

@app.route('/grupos/ver/<int:id>')
@login_required
def consultarGrupo(id):
    if (current_user.is_authenticated and (current_user.is_admin() or current_user.is_coordinador())):
        g = Grupo()
        p = Periodo()
        c = Carreras()
        return render_template('Grupo/Modificar.html', grupos=g.consultaIndividual(id), periodo=p.consultaGeneral(),carreras=c.consultaGeneral())
    else:
        abort(404)



@app.route('/grupos/guardar', methods=['post'])
@login_required
def editarGrupo():
    g=Grupo()
    g.idGrupo=request.form['id']
    g.idPeriodo=request.form['periodo']
    g.idCarrera=request.form['carrera']
    g.descripcion=request.form['descripcion']
    g.semestre=request.form['semestre']
    g.grupo=request.form['grupo']
    g.actualizar()
    flash('¡Grupo editado con éxito!')
    return redirect(url_for('grupos'))

@app.route('/grupos/eliminar/<int:id>')
@login_required
def eliminarGrupos(id):
    g=Grupo()
    g.eliminar(id)
    flash('¡Grupo eliminado con éxito!')
    return  redirect(url_for('grupos') )


#Fin
##############################################################################################



##############################################################################################
#Sección USUARIOS


@app.route('/usuarios/agregarAos', methods=['post'])
@login_required
def agregarUsuarios():
    u=Usuarios()
    u.nombre=request.form['nombre']
    u.sexo=request.form['sexo']
    u.telefono=request.form['telefono']
    u.email=request.form['email']
    u.contraseña=request.form['contraseña']
    u.tipo=request.form['tipo']
    u.insertar()
    flash('¡Datos personales registrados con éxito')
    return redirect(url_for('AlumnosNuevo'))

@app.route('/usuarios/agregarDoc', methods=['post'])
@login_required
def agregarUsuariosDoc():
    u=Usuarios()
    u.nombre=request.form['nombre']
    u.sexo=request.form['sexo']
    u.telefono=request.form['telefono']
    u.email=request.form['email']
    u.contraseña=request.form['contraseña']
    u.tipo=request.form['tipo']
    u.insertar()
    flash('¡Datos personales registrados con éxito')
    return redirect(url_for('docentesNuevo'))


@app.route('/usuarios/agregarCoor', methods=['post'])
@login_required
def agregarUsuariosCoor():
    u=Usuarios()
    u.nombre=request.form['nombre']
    u.sexo=request.form['sexo']
    u.telefono=request.form['telefono']
    u.email=request.form['email']
    u.contraseña=request.form['contraseña']
    u.tipo=request.form['tipo']
    u.insertar()
    flash('¡Datos personales registrados con éxito')
    return redirect(url_for('coordinadorNuevo'))

@app.route('/usuarios/editarPerfil')
@login_required
def editarPerfil():
    if(current_user.is_authenticated):
        return render_template('Usuarios/Modificar.html')
    else:
        abort(404)

@app.route('/usuarios/guardarPerfil' ,methods=['post'])
@login_required
def guardarPerfil():
    u=Usuarios()
    u=Usuarios()
    u.idUsuario=current_user.idUsuario
    u.nombre=request.form['nombre']
    u.sexo=request.form['sexo']
    u.telefono=request.form['telefono']
    u.email=current_user.email
    u.contraseña=request.form['contraseña']
    u.tipo=request.form['tipo']
    u.estatus=current_user.estatus

    u.actualizar()

    login_user(u)
    flash('¡Datos modificados con éxito!')
    return render_template('Usuarios/Modificar.html')

#Fin
########################################################################################################################
########################################################################################################################
#Sección de ERRORES
@app.errorhandler(404)
def error_404(e):
    return render_template('Comunes/error_404.html'),404

#Fin
########################################################################################################################
########################################################################################################################
#Sección Periodo

@app.route('/Periodos')
@login_required
def periodos():
    if (current_user.is_authenticated and (current_user.is_admin())):
        p=Periodo()
        periodo=p.consultaGeneral()
        return render_template('Periodo/Consulta.html', periodo=periodo)
    else:
        abort(404)



@app.route('/periodo/nuevo')
@login_required
def periodoNuevo():
    if (current_user.is_authenticated and (current_user.is_admin())):
        return render_template('Periodo/Nuevo.html')
    else:
        abort(404)


@app.route('/periodos/agregar', methods=['post'])
@login_required
def periodosAgregar():
    p=Periodo()
    p.nombre=request.form['nombre']
    p.fechaInicio=request.form['inicio']
    p.fechaFin=request.form['finaliza']
    p.insertar()
    flash('¡Período registrado con éxito!')
    return render_template('Periodo/Nuevo.html')

@app.route('/periodos/ver/<int:id>')
@login_required
def consultaPeriodos(id):
    if (current_user.is_authenticated and (current_user.is_admin())):
        p=Periodo()
        return render_template('Periodo/Modificar.html' , periodo=p.consultaIndividual(id))
    else:
        abort(404)

@app.route('/periodos/guardar', methods=['post'])
@login_required
def peridosModificar():
    p=Periodo()
    p.idPeriodo=request.form['idPeriodo']
    p.nombre=request.form['nombre']
    p.fechaInicio=request.form['inicio']
    p.fechaFin=request.form['finaliza']
    estatus = request.values.get('estatus', False)

    if estatus == "True":
        p.estatus = True
    else:
        p.estatus = False
    p.actualizar()

    flash('¡Período editado con éxito!')
    return redirect(url_for('periodos'))

@app.route('/periodos/eliminar/<int:id>')
@login_required
def eliminarPeriodos(id):
    p=Periodo()
    p.eliminar(id)
    flash('¡Periodo eliminada con éxito!')
    return redirect(url_for('periodos'))
#Fin
########################################################################################################################
########################################################################################################################





if __name__=='__main__':
    db.init_app(app)
    app.run(port=1000, debug=True,)

